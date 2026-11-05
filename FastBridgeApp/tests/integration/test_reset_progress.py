"""Route-level test for clearing recall progress (POST /userspace/reset_progress).

Drives the real userspace router with an in-process TestClient against a local Mongo. The
point of these tests is the *scope* of the delete: it has to take out the caller's rows for
the words in one list, and nothing else - not another user's identical row, not a homograph
filed under a gloss the list doesn't contain, not a word that lives in a different list.
Auth is overridden to a fixed test user and firebase_admin is stubbed so the router imports
without a service-account cert, mirroring test_submit_review.py. Skips when no local Mongo is
reachable, via the shared `mdt` fixture.
"""
import os
import sys
from datetime import datetime
from unittest.mock import MagicMock

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

sys.modules.setdefault("firebase_admin", MagicMock())
os.environ.setdefault("FIREBASE_CONFIG", "{}")

from fastapi import FastAPI
from fastapi.testclient import TestClient

TEST_UID = "reset-route-test-user"
OTHER_UID = "reset-route-other-user"
LIST_NAME = "Reset Test List"
BODY = {"language": "Latin", "list_name": LIST_NAME, "shared": False}

# The list holds amo/to love and video/to see. "amo/to like" is a homograph kept out of it
# on purpose, and "puella/girl" belongs to a different list.
LIST_WORDS = [["amo", "to love"], ["video", "to see"]]


def _meta(user_id, lemma, gloss, language="Latin"):
    return {
        "user_id": user_id, "language": language, "lemma": lemma, "gloss": gloss,
        "interval": 6, "ease": 2.5, "reps": 2, "lapses": 0,
        "due": datetime(2026, 1, 1), "last_review": datetime(2025, 12, 26),
    }


@pytest.fixture
def reset_client(mdt):
    for name in ("routers.userspace", "routers.select", "utils.study_meta"):
        sys.modules.pop(name, None)
    from routers import userspace
    from routers.firebase_auth import get_current_user_cookie
    from utils.study_meta import ensure_study_meta

    ensure_study_meta()

    app = FastAPI()
    app.include_router(userspace.router, prefix="/userspace")
    app.dependency_overrides[get_current_user_cookie] = lambda: {"uid": TEST_UID}

    storage = userspace.atlas_client.get_database("App-Storage")

    def _clean():
        storage.study_meta.delete_many({"user_id": {"$in": [TEST_UID, OTHER_UID]}})
        storage.lists.delete_many({"user_id": {"$in": [TEST_UID, OTHER_UID]}})

    _clean()
    storage.lists.insert_one({
        "user_id": TEST_UID,
        "languages": {"Latin": [
            {"name": LIST_NAME, "words": LIST_WORDS},
            {"name": "Another List", "words": [["puella", "girl"]]},
        ]},
    })
    yield TestClient(app), storage
    _clean()


def _keys(storage, user_id=TEST_UID):
    return sorted(
        (d["lemma"], d["gloss"])
        for d in storage.study_meta.find({"user_id": user_id}, {"_id": 0})
    )


def test_clears_the_lists_words_and_leaves_everything_else(reset_client):
    client, storage = reset_client
    storage.study_meta.insert_many([
        _meta(TEST_UID, "amo", "to love"),      # in the list -> goes
        _meta(TEST_UID, "video", "to see"),     # in the list -> goes
        _meta(TEST_UID, "amo", "to like"),      # homograph, not in the list -> stays
        _meta(TEST_UID, "puella", "girl"),      # a different list -> stays
        _meta(TEST_UID, "amo", "to love", language="Greek"),  # other language -> stays
    ])

    resp = client.post("/userspace/reset_progress", json=BODY)
    assert resp.status_code == 200
    assert resp.json() == {"success": True, "cleared": 2}

    assert _keys(storage) == [("amo", "to like"), ("amo", "to love"), ("puella", "girl")]
    # The surviving amo/to love is the Greek one, not a missed Latin row.
    langs = {d["language"] for d in storage.study_meta.find({"user_id": TEST_UID, "lemma": "amo", "gloss": "to love"})}
    assert langs == {"Greek"}


def test_another_users_identical_row_survives(reset_client):
    """Progress is per user, so resetting yours must not reach anyone else's."""
    client, storage = reset_client
    storage.study_meta.insert_many([
        _meta(TEST_UID, "amo", "to love"),
        _meta(OTHER_UID, "amo", "to love"),
    ])

    assert client.post("/userspace/reset_progress", json=BODY).json()["cleared"] == 1
    assert _keys(storage) == []
    assert _keys(storage, OTHER_UID) == [("amo", "to love")]


def test_untrimmed_stored_gloss_still_matches(reset_client):
    """study_pairs() strips the stored definition; the lookup has to agree, or a
    word saved with a stray space would be unresettable."""
    client, storage = reset_client
    storage.lists.update_one(
        {"user_id": TEST_UID},
        {"$set": {"languages.Latin.0.words": [["amo", "  to love  "]]}},
    )
    storage.study_meta.insert_one(_meta(TEST_UID, "amo", "to love"))

    assert client.post("/userspace/reset_progress", json=BODY).json()["cleared"] == 1
    assert _keys(storage) == []


def test_nothing_stored_is_not_an_error(reset_client):
    client, storage = reset_client

    resp = client.post("/userspace/reset_progress", json=BODY)
    assert resp.status_code == 200
    assert resp.json() == {"success": True, "cleared": 0}


def test_unknown_list_is_a_404(reset_client):
    client, storage = reset_client
    storage.study_meta.insert_one(_meta(TEST_UID, "amo", "to love"))

    resp = client.post("/userspace/reset_progress", json={**BODY, "list_name": "No Such List"})
    assert resp.status_code == 404
    # Nothing deleted on the way to the 404.
    assert _keys(storage) == [("amo", "to love")]


def test_missing_uid_is_unauthorized(mdt):
    for name in ("routers.userspace", "routers.select", "utils.study_meta"):
        sys.modules.pop(name, None)
    from routers import userspace
    from routers.firebase_auth import get_current_user_cookie

    app = FastAPI()
    app.include_router(userspace.router, prefix="/userspace")
    app.dependency_overrides[get_current_user_cookie] = lambda: {}

    resp = TestClient(app).post("/userspace/reset_progress", json=BODY)
    assert resp.status_code == 401
