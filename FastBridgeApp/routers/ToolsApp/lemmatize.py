"""This router replaces the old Lemmatizer. Will take in a text, as either html text input or as a file.
It will return a lemmatized sheet that will be ready to be sent to the importer once a human has resolved/deleted all the titles that resolved to NONE
"""

from fastapi import APIRouter, Request, File, Form, UploadFile
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
import importlib
import tempfile
from pathlib import Path
import re as regex
import unicodedata
import string
from typing import Optional

import stanza
import logging
logging.getLogger("stanza").setLevel(logging.WARNING)
logging.getLogger("stanza").setLevel(logging.ERROR)
logging.getLogger("stanza.pipeline").setLevel(logging.ERROR)

from cltk.lemmatize.lat import LatinBackoffLemmatizer
from cltk.lemmatize.grc import GreekBackoffLemmatizer

router = APIRouter()
router_path = Path.cwd()
templates = Jinja2Templates(directory="templates")

stanza_pipelines = {
    "latin": None,
    "greek": None
}

cltk_lemmatizers = {
    "latin": None,
    "greek": None,
}

# Invariable Latin words — hardcoded ground truth
LATIN_INVARIABLES = {
    "in": "in", "et": "et", "ab": "ab", "ad": "ad", "cum": "cum",
    "de": "de", "ex": "ex", "per": "per", "pro": "pro", "sub": "sub",
    "sed": "sed", "non": "non", "at": "at", "ac": "ac", "aut": "aut",
    "vel": "vel", "nec": "nec", "neque": "neque", "nam": "nam",
    "enim": "enim", "igitur": "igitur", "ergo": "ergo", "tamen": "tamen",
    "autem": "autem", "itaque": "itaque", "ante": "ante", "post": "post",
    "inter": "inter", "super": "super", "contra": "contra", "sine": "sine",
    "ob": "ob", "propter": "propter", "circa": "circa", "trans": "trans",
    "que": "que", "ve": "ve", "ne": "ne",
    "est": "sum", "sunt": "sum", "esse": "sum", "erat": "sum",
    "erant": "sum", "erit": "sum", "erunt": "sum", "fuit": "sum",
    "qui": "qui", "quae": "qui", "quod": "qui", "quem": "qui",
    "quam": "qui", "quo": "qui", "qua": "qui", "quos": "qui",
    "quas": "qui", "quibus": "qui", "cuius": "qui",
    "se": "se", "sibi": "se", "sui": "se",
}

# Invariable Greek words — hardcoded ground truth
GREEK_INVARIABLES = {
    "καί": "καί", "καὶ": "καί",
    "ὁ": "ὁ", "ἡ": "ὁ", "τό": "ὁ", "τόν": "ὁ", "τήν": "ὁ",
    "τοῦ": "ὁ", "τῆς": "ὁ", "τῷ": "ὁ", "τῇ": "ὁ",
    "τούς": "ὁ", "τάς": "ὁ", "τῶν": "ὁ", "τοῖς": "ὁ", "ταῖς": "ὁ",
    "τὸν": "ὁ", "τὴν": "ὁ", "τὸ": "ὁ",
    "ἐν": "ἐν", "εἰς": "εἰς", "ἐκ": "ἐκ", "ἐξ": "ἐκ",
    "ἀπό": "ἀπό", "ἀπὸ": "ἀπό",
    "πρός": "πρός", "πρὸς": "πρός",
    "διά": "διά", "διὰ": "διά",
    "μετά": "μετά", "μετὰ": "μετά",
    "κατά": "κατά", "κατὰ": "κατά",
    "παρά": "παρά", "παρὰ": "παρά",
    "περί": "περί", "περὶ": "περί",
    "ὑπό": "ὑπό", "ὑπὸ": "ὑπό",
    "ἐπί": "ἐπί", "ἐπὶ": "ἐπί",
    "δέ": "δέ", "δὲ": "δέ",
    "μέν": "μέν", "μὲν": "μέν",
    "οὐ": "οὐ", "οὐκ": "οὐ", "οὐχ": "οὐ",
    "μή": "μή", "μὴ": "μή",
    "γάρ": "γάρ", "γὰρ": "γάρ",
    "ἀλλά": "ἀλλά", "ἀλλὰ": "ἀλλά",
    "ὅτι": "ὅτι",
    "εἰ": "εἰ",
    "ὡς": "ὡς",
    "ἄρα": "ἄρα",
    "οὖν": "οὖν",
    "αὐτός": "αὐτός", "αὐτοῦ": "αὐτός", "αὐτῷ": "αὐτός",
    "αὐτόν": "αὐτός", "αὐτήν": "αὐτός", "αὐτό": "αὐτός",
    "αὐτὸς": "αὐτός", "αὐτὸν": "αὐτός",
}

# Inflected endings that mean CLTK returned the word unchanged
INFLECTED_ENDINGS = (
    "bant", "bat", "batur", "bantur",
    "erunt", "isse", "isset",
    "abant", "abatur",
    "entur", "antur", "itur", "untur",
    "amque", "asque", "osque", "isque",
    "esque", "oque", "aque",
)


def clean_cltk_lemma(lemma: str) -> str:
    return lemma.rstrip("0123456789")


def cltk_lemma_is_inflected(lemma: str, original_word: str) -> bool:
    if lemma != original_word:
        return False
    return any(original_word.endswith(ending) for ending in INFLECTED_ENDINGS)


def get_pipeline(language: str):
    global stanza_pipelines
    lang_code = {"latin": "la", "greek": "grc"}.get(language.lower())
    if not lang_code:
        raise ValueError(f"Unsupported language: {language}")
    if stanza_pipelines[language] is None:
        try:
            stanza.download(lang_code, verbose=False)
        except Exception as e:
            print(f"Warning: Stanza model for {lang_code} may already be present. ({e})")
        stanza_pipelines[language] = stanza.Pipeline(
            lang_code,
            processors="tokenize,mwt,pos,lemma",
            tokenize_no_ssplit=True
        )
    return stanza_pipelines[language]


def get_cltk_lemmatizer(language: str):
    global cltk_lemmatizers
    if language.lower() == "latin" and cltk_lemmatizers["latin"] is None:
        cltk_lemmatizers["latin"] = LatinBackoffLemmatizer()
    if language.lower() == "greek" and cltk_lemmatizers["greek"] is None:
        cltk_lemmatizers["greek"] = GreekBackoffLemmatizer()
    return cltk_lemmatizers.get(language.lower())


@router.get("/")
def lemma_index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("lemmatize.html", context)


@router.post("/")
async def lemmatizing_handler(
    request: Request,
    format: str = Form(...),
    language: str = Form(...),
    poetry: str = Form(...),
    resulting_filename: str = Form("tempfile"),
    text: str = Form(""),
    file: Optional[UploadFile] = File(...)
):
    lemma_lex = importlib.import_module(f'routers.ToolsApp.{language}_lemmata').LEMMATA
    poetry = poetry == 'Yes'
    resulting_filename += ".csv"
    work_file = tempfile.NamedTemporaryFile(suffix='.csv', dir='/tmp', delete=False)

    with work_file as outputfile:
        location = ""
        print(resulting_filename)
        print(outputfile.name)

        the_text = file.file.read()
        regex_go_brrr = regex.compile(r'\[[0-9]+(\_|\.?[0-9]+)*\]')

        if text and the_text != b'':
            return "Please choose just one input method."

        if text:
            csv_output = lemmatize(text, location, regex_go_brrr, language, lemma_lex, format, poetry)
            outputfile.write('﻿'.encode('utf-8'))
            outputfile.write(csv_output.encode('utf-8'))
        elif the_text:
            text = the_text.decode("utf-8")
            csv_output = lemmatize(text, location, regex_go_brrr, language, lemma_lex, format, poetry)
            outputfile.write('﻿'.encode('utf-8'))
            outputfile.write(csv_output.encode('utf-8'))
        else:
            return "Please enter or upload text."

        return FileResponse(f'{outputfile.name}', media_type='application/octet-stream', filename=resulting_filename)


def strip_accents(s: str):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def depunctuate(text: str):
    return regex.sub(f"[{string.punctuation}]", "", text)


def hybrid_lemmatize_word(word_clean: str, language: str, stanza_pipeline) -> str:
    """
    CLTK + Stanza hybrid for Latin and Greek.
    1. Invariables
    2. CLTK as primary
    3. Stanza as fallback
    """
    lang = language.lower()

    # Check invariables
    if lang == "latin" and word_clean in LATIN_INVARIABLES:
        return LATIN_INVARIABLES[word_clean]
    if lang == "greek" and word_clean in GREEK_INVARIABLES:
        return GREEK_INVARIABLES[word_clean]

    # Try CLTK
    cltk = get_cltk_lemmatizer(language)
    if cltk:
        results = cltk.lemmatize([word_clean])
        if results:
            cltk_lemma = clean_cltk_lemma(results[0][1])
            if lang == "latin":
                if cltk_lemma and not cltk_lemma_is_inflected(cltk_lemma, word_clean):
                    return cltk_lemma
            else:
                # For Greek, always trust CLTK if it returned something
                if cltk_lemma:
                    return cltk_lemma

    # Fall back to Stanza
    if stanza_pipeline:
        doc = stanza_pipeline(word_clean)
        for sent in doc.sentences:
            for w in sent.words:
                if w.lemma:
                    return w.lemma

    return "NONE"


def lemmatize(text, location, regex_go_brrr, language, lemma_lex, format, poetry):
    output_lines = ["TITLE,LOCATION,SECTION,RUNNINGCOUNT,TEXT"]
    running_count = 1
    section = 0

    conversion = importlib.import_module(f'routers.ToolsApp.{language}_morpheus_conversion').conversion_dict

    if poetry:
        lines = text.strip().splitlines()
        numbered_lines = [f"[{i+1}] {line}" for i, line in enumerate(lines)]
        text = " ".join(numbered_lines)

    text = text.replace(".", "_")
    words = text.split()

    stanza_pipeline = None
    if format.upper() in ("STANZA", "HYBRID"):
        stanza_pipeline = get_pipeline(language.lower())

    for word in words:
        word_original = word
        match_full = regex_go_brrr.fullmatch(word)
        match_start = regex_go_brrr.match(word)

        if match_full:
            location = match_full.group()[1:-1]
            section += 1
            continue
        elif match_start:
            marker = match_start.group()
            location = marker[1:-1]
            section += 1
            word = word.replace(marker, "")

        # For Greek, preserve accents — don't strip them
        if language.lower() == "greek":
            word_clean = depunctuate(word)
        else:
            word_clean = depunctuate(strip_accents(word)).lower()

        if not word_clean:
            continue

        if format.upper() == "HYBRID":
            lemma = hybrid_lemmatize_word(word_clean, language, stanza_pipeline)
            title = f"hybrid: {lemma}" if lemma != "NONE" else "hybrid: NONE"

        elif format.upper() == "STANZA" and stanza_pipeline is not None:
            doc = stanza_pipeline(word_clean)
            lemma = None
            for sent in doc.sentences:
                for w in sent.words:
                    if w.lemma:
                        lemma = w.lemma
                        break
            title = f"stanza: {lemma}" if lemma else "stanza: NONE"

        else:
            if word_clean in lemma_lex:
                title = lemma_lex[word_clean]
                title = conversion.get(title, f"morpheus: {title}")
            else:
                title = "morpheus: NONE"

        output_lines.append(f"{title},{location},{section},{running_count},{word_original}")
        running_count += 1

    return "\n".join(output_lines) + "\n"