"""Test-only FastAPI app for the Playwright e2e suite.

It mounts the app's routers so Playwright can drive the real pages without a Firebase config
or the torch-heavy NLP stack. Importing the real main.py fails without FIREBASE_CONFIG
(firebase_auth runs initialize_app() at import), and the lemmatizer imports Stanza/CLTK at
module load, so we neutralize both at the test layer here and build a smaller app. This is
test scaffolding, not production code.

The mounted routers connect to MongoDB at import, so a local Mongo must be running.
"""
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

# Point imports and the working directory at the app source, so bare imports and the
# cwd-relative templates/static paths resolve exactly like the real app does.
# parents[4] == repo root (this file is at FastBridgeApp/tests/e2e/harness/e2e_app.py).
FASTBRIDGE = Path(__file__).resolve().parents[4] / "FastBridgeApp"
sys.path.insert(0, str(FASTBRIDGE))
os.chdir(FASTBRIDGE)
os.environ.setdefault("MONGO_URI", "mongodb://localhost:27017")
os.environ.setdefault("MONGO_TLS", "false")

# --- test-layer stubs so the real routers import without their heavy/secret dependencies ----
# firebase_admin needs a service-account cert + network; the session-cookie auth we actually
# exercise doesn't use it at runtime (it's a Mongo-backed UUID). Stanza/CLTK are the torch
# stack the CI image intentionally omits. The Google Sheets client is imported at module load
# by about.py -> quickstart.py but only used by the /about/texts route, not the pages we scan.
# Stub them all before importing any router.
os.environ.setdefault("FIREBASE_CONFIG", "{}")
for _name in (
    "firebase_admin",
    "stanza",
    "cltk", "cltk.lemmatize", "cltk.lemmatize.lat", "cltk.lemmatize.grc",
    "cltk.utils", "cltk.data", "cltk.data.fetch",
    "googleapiclient", "googleapiclient.discovery",
    "google_auth_oauthlib", "google_auth_oauthlib.flow",
    "google", "google.auth", "google.auth.transport", "google.auth.transport.requests",
):
    sys.modules.setdefault(_name, MagicMock())

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routers import select, about, user_help, userspace
from routers.ToolsApp import lemmatize
from routers.firebase_auth import create_session, _set_session_cookie

app = FastAPI()
app.include_router(select.router, prefix="/select")
app.include_router(about.router, prefix="/about")
app.include_router(user_help.router, prefix="/help")
app.include_router(userspace.router, prefix="/userspace")
app.include_router(lemmatize.router, prefix="/lemmatizer")

templates = Jinja2Templates(directory="templates")
app.mount("/assets", StaticFiles(directory=str(Path("static") / "assets")), name="assets")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("list-index.html", {"request": request})


@app.get("/e2e-login")
def e2e_login():
    """Test-only: mint a real Mongo-backed session for a fixture user and set the cookie.

    Exists only in this harness app, never in production main.py. Playwright's global setup
    hits this once and saves the resulting cookies as storageState, so authed pages (userspace)
    load as a signed-in user without touching Firebase.
    """
    session_id = create_session("e2e-uid", "e2e@example.com", "E2E Tester")
    response = JSONResponse({"ok": True})
    _set_session_cookie(response, session_id, display_name="E2E Tester")
    return response
