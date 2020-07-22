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

@router.get("/user_guide")
def user_guide(request: Request):
    context = {'request' : request}
    return templates.TemplateResponse("user_help.html", context)


@router.get("/collaborate")
def colloborate(request: Request):
    context = {'request' : request}
    return templates.TemplateResponse("collaborate.html", context)

@router.get("/lemmatize")
def lemmatize_help(request: Request):
    context = {'request' : request}
    return templates.TemplateResponse("lemmatize_help.html", context)
