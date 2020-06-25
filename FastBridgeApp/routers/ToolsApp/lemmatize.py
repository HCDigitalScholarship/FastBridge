"""This router replaces the old Lemmatizer. Will take in a text, as either html text input or as a file. It will return a lemmatized sheet that will be ready to be sent to the importer once a human has resolved/deleted all the titles that resolved to NONE"""
from fastapi import APIRouter, WebSocket, Request, File, Form, UploadFile, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import importlib
import tempfile
from pathlib import Path
from pydantic import BaseModel
import re as regex
from starlette.responses import FileResponse
from typing import Optional
import unidecode
import string
router = APIRouter()
router_path = Path.cwd()
templates = Jinja2Templates(directory="templates")


@router.get("/Lemmatizer")
def lemma_index(request : Request):
    context= {"request" : request}
    return templates.TemplateResponse("lemmatize.html", context)
@router.post("/Lemmatizer")
async def lemmatizing_handler(request : Request, format : str =  Form(...), language : str = Form(...), resulting_filename : str =  Form("tempfile"), text : str = Form(""), file : UploadFile = File("file")):
    print(format)
    lemma_lex =  importlib.import_module(f'routers.ToolsApp.{language}_lemmata').LEMMATA
    #I think there is a nice way to pickle and unpickle this to save space, but i am not sure how to do that. Pickle was complaining for me.
    resulting_filename += ".csv"
    work_file = tempfile.NamedTemporaryFile(suffix='.csv',dir='/tmp', delete =  False)
    with work_file as outputfile:
        location = "" #calculate location at the start of each new section.
        #So for the start of the Metamorphoses, we want something like this: [1.1] In nova fert animus mutatas dicere formas [1.2] corpora; di, coeptis (nam vos mutastis et illas). Linebreaks should not matter
        print(resulting_filename)
        print(outputfile.name)
        regex_go_brrr = regex.compile('[0-9]+(\_?[0-9]+)*')
        if text and file.file.read():
            #raise some error, they should only fill in one of these fields
            print("got both")
            return "Please choose just one thank you"
        if text: #got the input as a string
            outputfile.write(lemmatize(text, location, regex_go_brrr, language, lemma_lex, format).encode('utf-8'))
        elif file:
            text = file.file.read().decode("utf-8") #reads the file as a string. I don't think this will cause problems with large inputs, but it potentially could, and then makes all of this much cleaner.
            print(text)
            outputfile.write(lemmatize(text, location, regex_go_brrr, language, lemma_lex, format).encode('utf-8'))
        else:
            #neither were given, which is also bad
            print(file)
            print("got neither")
            return False

        return FileResponse(f'{outputfile.name}', media_type='routerlication/octet-stream', filename = resulting_filename)



def demacronize(text : str , language : str):
    if language == "Latin":
        text= unidecode.unidecode(text) #the only magic left. This somehow removes all the macrons. It completely breaks Greek though
        text = text.replace("v", "u")
        text = text.replace("V", "U")
        text = text.replace("j", "i")
        text = text.replace("J", "I")
    elif language == "Greek":
        print(text)
    print(text)
    return text
def depunctuate(text : str):
    text = regex.sub(f"[{string.punctuation}]","" ,text)
    return text


def lemmatize(text, location, regex_go_brrr, language, lemma_lex, format):
    output = ""
    text.replace(".", "_")
    text =  text.split()
    running_count = 1 #if this started at 0, it would make some other things cleaner, but it already starts at 1 everywhere else so lets not change it.
    if format == "Bridge":
        #the default lemma_lex is the perseus one, if we get the equivalnces stored nicely in an other file as a dictionary, it will be best to just import that file and look up the conversion.
        pass
    for word in text:
        if regex_go_brrr.match(word):
            location = word
        else:
            location = location
            word = demacronize(word, language)
            word = depunctuate(word)
            try:
                title = lemma_lex[word]
            except KeyError:
                title =  "NONE" #humans will need to address this one!


            output += f'{title},{location},{running_count},{word}\n'
            running_count+=1
    return output
