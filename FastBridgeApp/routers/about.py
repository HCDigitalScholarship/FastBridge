from fastapi import APIRouter, WebSocket, Request, File, Form, UploadFile, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import importlib
import quickstart
from pathlib import Path
import DefinitionTools
router = APIRouter()
router_path = Path.cwd()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def render_about(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("about.html", context)


@router.get("/texts")
def about_the_texts(request: Request):
    context = {'request': request}
    data = quickstart.main()  # this is a list of all the texts that is stored in a google spreadsheet. Each row/item of this list has 24 items, consult the sheet
    table_headers = data[0]
    books_data = []
    for text in data[1:]:
        markup = ['<tr>']
        [markup.append(
            f"<td>{info}</td>") if info else markup.append(f"<td>No</td>") for info in text]
        markup.append('</tr>')
        markup = ''.join(markup)
        # print(markup)
        to_add = {"values": text, "markup": markup, "active": True}
        books_data.append(to_add)

    columns = {}
    headers = f''
    for i in range(len(table_headers)):
        print(table_headers[i])
        columns[table_headers[i]] = [True, True]
        headers += (
            f"<td onclick=\"sortTable(\'{table_headers[i]}\',{i})\">{table_headers[i]}</td>")

    context["books_data"] = books_data
    context["columns"] = columns
    context["headers"] = headers
    context["style"] = f'td{{max-width : 10vh; width: 10vh; color: white;}}'
    return templates.TemplateResponse("about_the_texts.html", context)

@router.get("/people")
def render_about(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("people.html", context)