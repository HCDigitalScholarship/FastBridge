from fastapi import APIRouter, WebSocket, Request, File, Form, UploadFile, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import importlib
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
        the_text =  get_text(text, language)
        markup = f"<tr> <td>{text}</td><td>{the_text.subsection}</td><td>{the_text.local_def}</td><td>{the_text.local_lem}</td></tr>"
        to_add = {"values" : [text, the_text.subsections, the_text.local_def, the_text.local_lem], "markup" : markup, "active" : True} #this is to make it searchable like the Lists result table, there will eventually be hundreds of texts.
        books_data.append(to_add)
        del the_text

    context["books_data"] = books_data
    return templates.TemplateResponse("about_the_texts.html", context)
