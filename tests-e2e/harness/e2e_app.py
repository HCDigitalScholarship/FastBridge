"""Test-only FastAPI app for the Playwright e2e suite.

It mounts only the non-auth routers so Playwright can drive the real pages without a
Firebase config. Importing the real main.py fails without FIREBASE_CONFIG (firebase_auth
runs initialize_app() at import), so we build a smaller app here instead. This is test
scaffolding, not production code.

The mounted routers connect to MongoDB at import, so a local Mongo must be running.
"""
import os
import sys
from pathlib import Path

# Point imports and the working directory at the app source, so bare imports and the
# cwd-relative templates/static paths resolve exactly like the real app does.
FASTBRIDGE = Path(__file__).resolve().parents[2] / "FastBridgeApp"
sys.path.insert(0, str(FASTBRIDGE))
os.chdir(FASTBRIDGE)
os.environ.setdefault("MONGO_URI", "mongodb://localhost:27017")
os.environ.setdefault("MONGO_TLS", "false")

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routers import select, about, user_help

app = FastAPI()
app.include_router(select.router, prefix="/select")
app.include_router(about.router, prefix="/about")
app.include_router(user_help.router, prefix="/help")

templates = Jinja2Templates(directory="templates")
app.mount("/assets", StaticFiles(directory=str(Path("static") / "assets")), name="assets")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("list-index.html", {"request": request})
