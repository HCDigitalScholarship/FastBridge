from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
import uvicorn
from routers.ToolsApp import lemmatize
from routers import oracle, select, about, user_help, stats, firebase_auth, userspace, lemma_workspace


async def not_found(request, exc):
    context = {"request": request}
    context["statuscode"] = 404
    return templates.TemplateResponse("notfound.html", context)

async def server_error(request, exc):
    context = {"request": request}
    print(exc)
    context["statuscode"] = 500
    return templates.TemplateResponse("notfound.html", context)

async def invalid_accesss(request, exc):
    context = {"request": request, "detail": exc.detail}
    context["statuscode"] = 401
    return templates.TemplateResponse("notfound.html", context)

exception_handlers = {
    404: not_found,
    500: server_error,
    401: invalid_accesss
}

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, exception_handlers=exception_handlers)

app.include_router(lemmatize.router, prefix="/lemmatizer", tags=["lemmatize"])
app.include_router(firebase_auth.router, prefix = "/account", tags=["account"])
app.include_router(userspace.router, prefix = "/userspace", tags=["userspace"])
app.include_router(oracle.router, prefix = "/oracle", tags=["oracle"])
app.include_router(select.router, prefix = "/select", tags=["select"])
app.include_router(about.router, prefix = "/about", tags=["about"])
app.include_router(user_help.router, prefix = "/help", tags=["help"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])
app.include_router(lemma_workspace.router, prefix="/lemma-workspace", tags=["lemma-workspace"])

templates = Jinja2Templates(directory="templates")
app_path = Path.cwd()

static_path = app_path / "static" / "assets"
app.mount("/assets", StaticFiles(directory=static_path), name="assets")

plot_path = static_path / "plots"
app.mount("/plots", StaticFiles(directory=plot_path), name="plots")

@app.get("/")
async def index(request : Request):
    return templates.TemplateResponse("list-index.html", {"request": request})

@app.get("/demacronizer", response_class=HTMLResponse)
async def index(request : Request):
    return templates.TemplateResponse("demacronizer.html", {"request": request})

if __name__ == '__main__':
    uvicorn.run("main:app", reload = True, host="64.227.97.179")
