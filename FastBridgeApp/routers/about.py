from fastapi import APIRouter, WebSocket, Request, File, Form, UploadFile, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import importlib

from pathlib import Path
import DefinitionTools
router = APIRouter()
router_path = Path.cwd()
templates = Jinja2Templates(directory="templates")
@router.get("/")
def render_about(request: Request):
    context = {'request' : request}
    return templates.TemplateResponse("about.html", context)



@router.get("/texts")
def about_the_texts(request: Request):
    context = {'request' : request}
    return templates.TemplateResponse("about_lang_choice.html", context)

@router.get("/texts/{language}")
def about_the_texts_lang(request: Request, language: str):
    context = {'request' : request}
    the_text_names = importlib.import_module(f'data.{language}.texts').texts
    books_data = []
    for text in the_text_names:
        computer_name =  text.lower().replace(" ", "_").replace(",","").replace(":","") #copy-pasted from add_new_text.py and should be – that is our gold standard for going from human names to machine names
        the_text =  DefinitionTools.get_text(computer_name, language).book
        if the_text.local_def:
            bool1 = "Yes"
        else:
            bool1 = "No"
        if the_text.local_lem:
            bool2 = "Yes"
        else:
            bool2 = "No"
        markup = f"<tr> <td>{text}</td><td>{the_text.subsections}</td><td>{bool1}</td><td>{bool2}</td></tr>"
        to_add = {"values" : [text, the_text.subsections, bool1, bool2], "markup" : markup, "active" : True} #this is to make it searchable like the Lists result table, there will eventually be hundreds of texts.
        books_data.append(to_add)
        del the_text

    context["books_data"] = books_data
    context["language"] = language
    context["columns"] = {"Title" : [True, True], "Subsection_Depth" : [True, True], "local_def" : [True, True], "local_lem" : [True, True]}
    context["style"] = f'td{{max-width : 100px; width: 100px; color: white}}'
    return templates.TemplateResponse("about_the_texts.html", context)
