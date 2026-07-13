"""This router replaces the old Lemmatizer. Will take in a text, as either html text input or as a file.
It will return a lemmatized sheet that will be ready to be sent to the importer once a human has resolved/deleted all the titles that resolved to NONE
"""

from fastapi import APIRouter, Request, File, Form, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from starlette.responses import FileResponse
import importlib
import os
import tempfile
from pathlib import Path
import re as regex
import unicodedata
import string
from urllib.parse import quote
from typing import Optional

import stanza
import logging
logging.getLogger("stanza").setLevel(logging.WARNING)
logging.getLogger("stanza").setLevel(logging.ERROR)
logging.getLogger("stanza.pipeline").setLevel(logging.ERROR)

from cltk.lemmatize.lat import LatinBackoffLemmatizer
from cltk.lemmatize.grc import GreekBackoffLemmatizer
from cltk.utils import CLTK_DATA_DIR
from cltk.data.fetch import FetchCorpus
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
# CLTK backoff-lemmatizer corpora, fetched into ~/cltk_data on demand
CLTK_CORPORA = {
    "latin": ("lat", "lat_models_cltk"),
    "greek": ("grc", "grc_models_cltk"),
}

# Logeion dictionary base URL — lemma is appended directly
LOGEION_BASE_URL = "https://logeion.uchicago.edu/"

# Tool prefixes that may be attached to the TITLE column
TOOL_PREFIXES = ("hybrid", "stanza", "morpheus")

# Greek sentence punctuation that string.punctuation does NOT cover.
# Defined via code points to avoid two visually-identical dot characters in
# source: middle dot (U+00B7) and the Greek ano teleia (U+0387). Without
# stripping these, tokens like "Kyros·" never match the lexicon and carry the
# dot into both the lemma and the Logeion URL.
GREEK_PUNCTUATION = chr(0x00B7) + chr(0x0387)


def _ensure_cltk_corpus(language: str):
    """Download the CLTK backoff corpus for `language` if it isn't already
    present. Mirrors the runtime stanza.download() pattern in get_pipeline().
    No-op when the corpus was baked into the image at build time."""
    lang_code, corpus_name = CLTK_CORPORA[language.lower()]
    model_dir = os.path.join(CLTK_DATA_DIR, lang_code, "model", corpus_name)
    if not os.path.isdir(model_dir):
        try:
            FetchCorpus(lang_code).import_corpus(corpus_name)
        except Exception as e:
            print(f"Warning: could not fetch CLTK corpus {corpus_name}: {e}")

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
    # elided form: depunctuate() removes the apostrophe in "δ'", leaving a bare δ
    "δ": "δέ",
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


def split_title(title: str):
    """Split a TITLE column value into (tool, lemma).

    Titles look like "hybrid: amor", "stanza: amor", or "morpheus: amor".
    Some morpheus titles come straight from the conversion dict and have no
    prefix at all, in which case tool is "" and the whole value is the lemma.
    """
    for tool in TOOL_PREFIXES:
        prefix = f"{tool}: "
        if title.startswith(prefix):
            return tool, title[len(prefix):]
    return "", title


def build_logeion_url(lemma: str) -> str:
    """Construct a Logeion dictionary URL for a lemma (Latin or Greek).
    Greek lemmas are polytonic Unicode, so the path segment is percent-encoded."""
    return LOGEION_BASE_URL + quote(lemma.strip())


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
        # No tokenize_no_ssplit here: we now feed Stanza the WHOLE text at once,
        # so we want it to split sentences and lemmatize each word in context.
        stanza_pipelines[language] = stanza.Pipeline(
            lang_code,
            processors="tokenize,mwt,pos,lemma",
        )
    return stanza_pipelines[language]


def get_cltk_lemmatizer(language: str):
    global cltk_lemmatizers
    if language.lower() == "latin" and cltk_lemmatizers["latin"] is None:
        _ensure_cltk_corpus("latin")
        cltk_lemmatizers["latin"] = LatinBackoffLemmatizer()
    if language.lower() == "greek" and cltk_lemmatizers["greek"] is None:
        _ensure_cltk_corpus("greek")
        cltk_lemmatizers["greek"] = GreekBackoffLemmatizer()
    return cltk_lemmatizers.get(language.lower())


# ----------------------------------------------------------------------------
# Ensemble helpers: CLTK + Stanza cross-checked for a confidence signal.
# ----------------------------------------------------------------------------

def _clean_form(word: str, language: str) -> str:
    """Compute the same 'word_clean' key used when iterating the text, so a
    Stanza token can be looked up by the form our loop produces."""
    if language.lower() == "greek":
        return depunctuate(word)
    return depunctuate(strip_accents(word)).lower()


def build_stanza_lemma_map(text: str, language: str) -> dict:
    """Run Stanza ONCE over the whole text (so every word is lemmatized in
    context, and we don't pay the neural cost per word). Returns a
    {clean_form: lemma} lookup keyed the same way the main loop keys words."""
    lang = language.lower()
    mapping = {}
    try:
        pipeline = get_pipeline(lang)
        doc = pipeline(text)
    except Exception as e:
        print(f"Warning: Stanza failed on the full text: {e}")
        return mapping

    for sent in doc.sentences:
        for w in sent.words:
            if not w.lemma:
                continue
            key = _clean_form(w.text, language)
            if key and key not in mapping:
                mapping[key] = w.lemma
    return mapping


def cltk_lemma_for(word_clean: str, language: str, cltk) -> str:
    """CLTK's lemma for a cleaned word, or '' on failure. For Latin, a return
    equal to the (inflected) input counts as a failure."""
    if not cltk:
        return ""
    results = cltk.lemmatize([word_clean])
    if not results:
        return ""
    lemma = clean_cltk_lemma(results[0][1])
    if not lemma:
        return ""
    if language.lower() == "latin" and cltk_lemma_is_inflected(lemma, word_clean):
        return ""
    return lemma


def _normalize_for_compare(lemma: str, language: str) -> str:
    """Loosely normalize a lemma so CLTK and Stanza can be compared without
    spurious disagreements (case, accents, i/j & u/v, trailing digits)."""
    if not lemma:
        return ""
    l = clean_cltk_lemma(lemma.strip())
    l = strip_accents(l).lower()
    if language.lower() == "latin":
        l = l.replace("j", "i").replace("v", "u")
    return l


def resolve_ensemble(word: str, word_clean: str, language: str, cltk, stanza_map: dict):
    """Combine invariables + CLTK + Stanza.

    Returns (lemma, confidence, cltk_lemma, stanza_lemma) where confidence is:
      'high'   — invariable, or CLTK and Stanza agree
      'review' — CLTK and Stanza disagree (best guess chosen; flag for a human)
      'medium' — only one tool resolved it
      'none'   — nothing resolved it
    """
    lang = language.lower()

    # 1. Authoritative hand-built table
    if lang == "latin" and word_clean in LATIN_INVARIABLES:
        return LATIN_INVARIABLES[word_clean], "high", "", ""
    if lang == "greek" and word_clean in GREEK_INVARIABLES:
        return GREEK_INVARIABLES[word_clean], "high", "", ""

    c = cltk_lemma_for(word_clean, language, cltk)
    s = stanza_map.get(word_clean, "")

    if c and s:
        if _normalize_for_compare(c, language) == _normalize_for_compare(s, language):
            return c, "high", c, s
        # Disagreement: prefer Stanza for proper-noun-looking (capitalized)
        # tokens, which is where CLTK is weakest; otherwise trust CLTK.
        chosen = s if word[:1].isupper() else c
        return chosen, "review", c, s
    if c:
        return c, "medium", c, ""
    if s:
        return s, "medium", "", s
    return "NONE", "none", "", ""


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


@router.post("/json")
async def lemmatizing_json_handler(
    request: Request,
    format: str = Form(...),
    language: str = Form(...),
    poetry: str = Form(...),
    resulting_filename: str = Form("tempfile"),
    text: str = Form(""),
    file: Optional[UploadFile] = File(None),
):
    """Same processing as the CSV endpoint, but returns display 'segments' as
    JSON so the frontend can render the text either as running paragraphs or as
    a table, with a per-word confidence. The CSV endpoint is left untouched."""
    lemma_lex = importlib.import_module(f'routers.ToolsApp.{language}_lemmata').LEMMATA
    poetry_bool = poetry == 'Yes'
    location = ""
    regex_go_brrr = regex.compile(r'\[[0-9]+(\_|\.?[0-9]+)*\]')

    the_text = b''
    if file is not None:
        the_text = file.file.read()

    if text and the_text != b'':
        return JSONResponse({"error": "Please choose just one input method."}, status_code=400)

    if text:
        source = text
    elif the_text:
        source = the_text.decode("utf-8")
    else:
        return JSONResponse({"error": "Please enter or upload text."}, status_code=400)

    annotated = lemmatize_annotate(source, location, regex_go_brrr, language, lemma_lex, format, poetry_bool)
    segments = annotated["segments"]

    word_segments = [s for s in segments if s["t"] == "w"]
    none_count = sum(1 for s in word_segments if s["none"])
    review_count = sum(1 for s in word_segments if s.get("conf") == "review")

    return JSONResponse({
        "language": language,
        "format": format,
        "count": len(word_segments),
        "none_count": none_count,
        "review_count": review_count,
        "segments": segments,
    })


def strip_accents(s: str):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def depunctuate(text: str):
    """Remove ASCII punctuation plus Greek sentence punctuation (middle dot /
    ano teleia) that string.punctuation misses."""
    return regex.sub(f"[{string.punctuation}{GREEK_PUNCTUATION}]", "", text)


def lemmatize_annotate(text, location, regex_go_brrr, language, lemma_lex, format, poetry):
    """Core lemmatization loop. Single pass producing two things:

      rows     — one dict per lemmatized token (title/location/section/
                 running_count/text). Feeds the CSV endpoint via lemmatize().
      segments — the original text broken into ordered pieces that preserve
                 whitespace and line breaks, so the frontend can render the
                 text as paragraphs or as a table, with a per-word confidence.

    For the Hybrid format, CLTK and Stanza are BOTH consulted for every word:
    Stanza runs once over the whole text (context + speed), CLTK runs per word,
    and their agreement drives a confidence level.

    Segment shapes:
      {"t": "s", "x": "<whitespace>"}                       literal spacing
      {"t": "b", "loc": "<n>"}                              line break (poetry marker)
      {"t": "x", "x": "<token>"}                            non-lemmatized token (punctuation, etc.)
      {"t": "w", "x", "lemma", "logeion", "none", "loc", "n",
       "conf", ["cltk","stanza" when conf=="review"]}       a lemmatized word
    """
    rows = []
    segments = []
    running_count = 1
    section = 0

    conversion = importlib.import_module(f'routers.ToolsApp.{language}_morpheus_conversion').conversion_dict

    fmt = format.upper()
    is_hybrid = "HYBRID" in fmt
    use_stanza = is_hybrid or "STANZA" in fmt

    # Run Stanza once over the ORIGINAL text (before we insert poetry markers or
    # swap periods for underscores), so it tokenizes and lemmatizes naturally.
    stanza_map = build_stanza_lemma_map(text, language) if use_stanza else {}
    cltk = get_cltk_lemmatizer(language) if is_hybrid else None

    if poetry:
        lines = text.strip().splitlines()
        numbered_lines = [f"[{i+1}] {line}" for i, line in enumerate(lines)]
        text = " ".join(numbered_lines)

    text = text.replace(".", "_")

    # Split on whitespace but KEEP it, so the original layout can be rebuilt.
    # The word tokens are identical to text.split(), so rows stay unchanged.
    for part in regex.split(r'(\s+)', text):
        if part == "":
            continue
        if part.isspace():
            segments.append({"t": "s", "x": part})
            continue

        word_original = part
        word = part
        match_full = regex_go_brrr.fullmatch(word)
        match_start = regex_go_brrr.match(word)

        if match_full:
            location = match_full.group()[1:-1]
            section += 1
            segments.append({"t": "b", "loc": location})
            continue
        elif match_start:
            marker = match_start.group()
            location = marker[1:-1]
            section += 1
            segments.append({"t": "b", "loc": location})
            word = word.replace(marker, "")

        word_clean = _clean_form(word, language)

        if not word_clean:
            # Punctuation-only or empty after cleaning — render as plain text.
            segments.append({"t": "x", "x": word})
            continue

        conf = None
        cltk_alt = ""
        stanza_alt = ""

        if is_hybrid:
            lemma, conf, cltk_alt, stanza_alt = resolve_ensemble(word, word_clean, language, cltk, stanza_map)
            title = f"hybrid: {lemma}"

        elif "STANZA" in fmt:
            s = stanza_map.get(word_clean, "")
            lemma = s if s else "NONE"
            title = f"stanza: {lemma}" if s else "stanza: NONE"
            conf = "medium" if s else "none"

        else:
            if word_clean in lemma_lex:
                title = lemma_lex[word_clean]
                title = conversion.get(title, f"morpheus: {title}")
            else:
                title = "morpheus: NONE"

        row = {
            "title": title,
            "location": location,
            "section": section,
            "running_count": running_count,
            "text": word_original,
            "conf": conf,
        }
        if conf == "review":
            row["cltk"] = cltk_alt
            row["stanza"] = stanza_alt
        rows.append(row)

        _tool, disp_lemma = split_title(title)
        is_none = disp_lemma.strip().upper() == "NONE"
        seg = {
            "t": "w",
            "x": word.strip(string.punctuation + GREEK_PUNCTUATION),
            "lemma": disp_lemma,
            "logeion": None if is_none else build_logeion_url(disp_lemma),
            "none": is_none,
            "loc": location,
            "n": running_count,
        }
        if conf:
            seg["conf"] = conf
        if conf == "review":
            # Both candidate lemmas, each with its own Logeion link, so the UI
            # can show both and the reader can look up either and choose.
            seg["cltk"] = cltk_alt
            seg["stanza"] = stanza_alt
            seg["cltk_logeion"] = build_logeion_url(cltk_alt) if cltk_alt else None
            seg["stanza_logeion"] = build_logeion_url(stanza_alt) if stanza_alt else None
        segments.append(seg)
        running_count += 1

    return {"rows": rows, "segments": segments}


def lemmatize_rows(text, location, regex_go_brrr, language, lemma_lex, format, poetry):
    """Thin wrapper kept for the CSV path — returns just the rows."""
    return lemmatize_annotate(text, location, regex_go_brrr, language, lemma_lex, format, poetry)["rows"]


def _csv_field(value) -> str:
    """Quote a CSV field if it contains a comma, quote, or newline (standard
    RFC-4180 escaping). Without this, a word that keeps trailing punctuation
    like "tres," injects a phantom comma and misaligns every later column."""
    s = "" if value is None else str(value)
    if any(ch in s for ch in (",", '"', "\n", "\r")):
        return '"' + s.replace('"', '""') + '"'
    return s


def lemmatize(text, location, regex_go_brrr, language, lemma_lex, format, poetry):
    """Build the CSV string. Delegates the actual lemmatization to
    lemmatize_rows() so the CSV and JSON endpoints stay in sync.

    LOGEION and CONFIDENCE columns are appended at the end (after the original
    five columns, so positional importers reading columns 0-4 are unaffected).
    LOGEION is the dictionary URL for each resolved lemma (blank for NONE);
    CONFIDENCE is high / review / medium / none for Hybrid & Stanza (blank for
    the Bridge format). For disagreements (CONFIDENCE=review) the CLTK, CLTK_LOGEION,
    STANZA, and STANZA_LOGEION columns hold both candidate lemmas and their Logeion
    links (blank otherwise). Every field is CSV-quoted when needed so trailing
    punctuation in the TEXT column can't shift columns."""
    output_lines = [
        "TITLE,LOCATION,SECTION,RUNNINGCOUNT,TEXT,LOGEION,CONFIDENCE,"
        "CLTK,CLTK_LOGEION,STANZA,STANZA_LOGEION"
    ]
    rows = lemmatize_rows(text, location, regex_go_brrr, language, lemma_lex, format, poetry)
    for row in rows:
        _tool, lemma = split_title(row["title"])
        is_none = lemma.strip().upper() == "NONE"
        logeion = "" if is_none else build_logeion_url(lemma)
        conf = row.get("conf") or ""
        cltk_lem = row.get("cltk") or ""
        stanza_lem = row.get("stanza") or ""
        cltk_log = build_logeion_url(cltk_lem) if cltk_lem else ""
        stanza_log = build_logeion_url(stanza_lem) if stanza_lem else ""
        fields = [
            row["title"], row["location"], row["section"], row["running_count"],
            row["text"], logeion, conf, cltk_lem, cltk_log, stanza_lem, stanza_log,
        ]
        output_lines.append(",".join(_csv_field(f) for f in fields))
    return "\n".join(output_lines) + "\n"