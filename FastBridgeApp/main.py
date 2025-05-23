from fastapi import FastAPI, WebSocket, Request, File, Form, UploadFile, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import importlib
import DefinitionTools
from pathlib import Path
from pydantic import BaseModel
import add_new_text
import uvicorn
import secrets
from fastapi.responses import RedirectResponse
from typing import Optional
from routers.ToolsApp import lemmatize
from routers.sql_app import account
from routers import oracle, select, about, user_help,export, stats
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from starlette.applications import Starlette

async def not_found(request, exc):
    context = {"request": request}
    context["statuscode"] = 404
    return templates.TemplateResponse("notfound.html", context)

async def server_error(request, exc):
    context = {"request": request}
    print(exc)
    context["statuscode"] = 500
    return templates.TemplateResponse("notfound.html", context)

exception_handlers = {
    404: not_found,
    500: server_error
}

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, exception_handlers=exception_handlers)
# app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

app.include_router(lemmatize.router, prefix="/lemmatizer", tags=["lemmatize"])
app.include_router(account.router, prefix = "/account", tags=["account"])
app.include_router(oracle.router, prefix = "/oracle", tags=["oracle"])
app.include_router(select.router, prefix = "/select", tags=["select"])
app.include_router(about.router, prefix = "/about", tags=["about"])
app.include_router(user_help.router, prefix = "/help", tags=["help"])
app.include_router(export.router, prefix = "/export", tags=["export"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])

templates = Jinja2Templates(directory="templates")
app_path = Path.cwd()

static_path = app_path / "static" / "assets"
app.mount("/assets", StaticFiles(directory=static_path), name="assets")

plot_path = static_path / "plots"
app.mount("/plots", StaticFiles(directory=plot_path), name="plots")#for stats

@app.get("/")
async def index(request : Request):
    print(request['path'])
    return templates.TemplateResponse("list-index.html", {"request": request})
    #buttons clicked on this page will take us to /select/{language}


if __name__ == '__main__':
    uvicorn.run("main:app", reload = True, host="64.227.97.179")
 #End of select (or main?) code
