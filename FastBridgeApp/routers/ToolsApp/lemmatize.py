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

router = APIRouter()
router_path = Path.cwd()
templates = Jinja2Templates(directory="templates")

stanza.download("la")
stanza.download("grc")

stanza_pipelines = {
    "latin": stanza.Pipeline("la", processors="tokenize,mwt,pos,lemma", tokenize_no_ssplit=True),
    "greek": stanza.Pipeline("grc", processors="tokenize,mwt,pos,lemma", tokenize_no_ssplit=True)
}

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

        if text:  # input from form
            csv_output = lemmatize(text, location, regex_go_brrr, language, lemma_lex, format, poetry)
            outputfile.write('\ufeff'.encode('utf-8'))
            outputfile.write(csv_output.encode('utf-8'))
        elif the_text:  # input from file
            text = the_text.decode("utf-8")
            csv_output = lemmatize(text, location, regex_go_brrr, language, lemma_lex, format, poetry)
            outputfile.write('\ufeff'.encode('utf-8'))
            outputfile.write(csv_output.encode('utf-8'))
        else:
            return "Please enter or upload text."

        return FileResponse(f'{outputfile.name}', media_type='application/octet-stream', filename=resulting_filename)


def strip_accents(s: str):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def depunctuate(text: str):
    return regex.sub(f"[{string.punctuation}]", "", text)


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

    stanza_pipeline = stanza_pipelines.get(language.lower())

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

        word_clean = depunctuate(strip_accents(word)).lower()
        if not word_clean:
            continue

        if word_clean in lemma_lex and format.upper() != "STANZA":
            title = lemma_lex[word_clean]
            title = conversion.get(title, f"morpheus: {title}")
        else:
            title = "morpheus: NONE"
        if format.upper() == "STANZA" and stanza_pipeline is not None:
            doc = stanza_pipeline(word_clean)
            lemma = None
            for sent in doc.sentences:
                for w in sent.words:
                    if w.text.lower() == word_clean:
                        lemma = w.lemma
                        break
            if lemma:
                title = f"stanza: {lemma}"
            else:
                title = "stanza: NONE"

        output_lines.append(f"{title},{location},{section},{running_count},{word_original}")
        running_count += 1

    return "\n".join(output_lines) + "\n"
