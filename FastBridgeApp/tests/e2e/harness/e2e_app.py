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

from mongo_connection import atlas_client, dict_db
from routers import select, about, user_help, userspace
from routers.ToolsApp import lemmatize
from routers.firebase_auth import create_session, _set_session_cookie

E2E_UID = "e2e-uid"
E2E_LIST = "E2E Study List"
E2E_DICT_WORDS = [
    {
        "TITLE": "e2e-amo", "PRINCIPAL_PARTS": "amō, amāre, amāvī, amātus",
        "PRINCIPAL_PARTS_NO_DIACRITICALS": "amo, amare, amavi, amatus",
        "SIMPLE_LEMMA": "e2e-amo", "SHORT_DEFINITION": "to love",
        "LONG_DEFINITION": "to love, like, be fond of", "PART_OF_SPEECH": "Verb",
        "LOGEION_LINK": "", "FORCELLINI_LINK": "",
        "CONJUGATION": "1", "DECLENSION": "", "PROPER": "", "REGULAR": "T", "STOPWORD": "",
    },
    {
        "TITLE": "e2e-puella", "PRINCIPAL_PARTS": "puella, puellae",
        "PRINCIPAL_PARTS_NO_DIACRITICALS": "puella, puellae",
        "SIMPLE_LEMMA": "e2e-puella", "SHORT_DEFINITION": "girl",
        "LONG_DEFINITION": "a girl, maiden", "PART_OF_SPEECH": "Noun",
        "LOGEION_LINK": "", "FORCELLINI_LINK": "",
        "CONJUGATION": "", "DECLENSION": "1", "PROPER": "", "REGULAR": "T", "STOPWORD": "",
    },
]

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
    session_id = create_session(E2E_UID, "e2e@example.com", "E2E Tester")
    response = JSONResponse({"ok": True})
    _set_session_cookie(response, session_id, display_name="E2E Tester")
    return response


@app.get("/e2e-seed-list")
def e2e_seed_list():
    """Test: give the fixture user one saved Latin list the study page can render.

    /userspace/list/{language}/{list_name} resolves its words against the real
    bridge_latin_dictionary, so the a11y scan of that page needs both a `lists` document and
    matching dictionary entries. Idempotent, so re-running the suite is fine.

    Only ever touches the E2E fixture user's own list and the two "e2e-" dictionary entries,
    so running it against a populated local dictionary adds two rows and changes nothing real.
    """
    for word in E2E_DICT_WORDS:
        dict_db["bridge_latin_dictionary"].replace_one(
            {"TITLE": word["TITLE"]}, word, upsert=True
        )
    storage = atlas_client.get_database("App-Storage")
    storage.lists.update_one(
        {"user_id": E2E_UID},
        {"$set": {"languages.Latin": [{
            "name": E2E_LIST,
            "words": [[w["SIMPLE_LEMMA"], w["SHORT_DEFINITION"]] for w in E2E_DICT_WORDS],
        }]}},
        upsert=True,
    )
    # Recall progress is per user and per word, so clear it too: a leftover schedule from a
    # previous run would change which cards a fresh session offers.
    storage.study_meta.delete_many({"user_id": E2E_UID})
    return JSONResponse({"ok": True, "list_name": E2E_LIST})
