"""Route-level test for recall-mode persistence (POST /userspace/submit_review).

Drives the real userspace router with an in-process TestClient against a local Mongo, so it
covers the endpoint wiring - request -> upsert into study_meta keyed on
(user_id, language, lemma, gloss) - rather than the scheduler in isolation (that is
tests/unit/test_srs.py). Auth is overridden to a fixed test user and firebase_admin is
stubbed so the router imports without a service-account cert, mirroring
test_userspace_star_route.py. Skips when no local Mongo is reachable, via the shared `mdt`
fixture.
"""
import os
import sys
from unittest.mock import MagicMock

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

# Same import-time guards as test_userspace_star_route.py: userspace.py does
# `from firebase_admin import auth`, and firebase_auth.py parses FIREBASE_CONFIG.
sys.modules.setdefault("firebase_admin", MagicMock())
os.environ.setdefault("FIREBASE_CONFIG", "{}")

from fastapi import FastAPI
from fastapi.testclient import TestClient

TEST_UID = "review-route-test-user"
BODY = {"language": "Latin", "lemma": "amo", "gloss": "to love", "rating": "good"}


@pytest.fixture
def review_client(mdt):
    # `mdt` has bound mongo_connection to the local Mongo; import the router fresh so it
    # picks up that binding rather than a stale module from an earlier test.
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
    storage.study_meta.delete_many({"user_id": TEST_UID})
    yield TestClient(app), storage
    storage.study_meta.delete_many({"user_id": TEST_UID})


def _docs(storage):
    return list(storage.study_meta.find({"user_id": TEST_UID}, {"_id": 0}))


def test_first_review_creates_a_document(review_client):
    client, storage = review_client

    resp = client.post("/userspace/submit_review", json=BODY)
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    assert resp.json()["interval"] == 1

    docs = _docs(storage)
    assert len(docs) == 1
    assert docs[0]["lemma"] == "amo" and docs[0]["gloss"] == "to love"
    assert docs[0]["reps"] == 1 and docs[0]["lapses"] == 0
    # The point of the collection is range queries on `due`, so it has to be a
    # real BSON date, not the ISO string the `lists` collection stores.
    assert isinstance(docs[0]["due"], __import__("datetime").datetime)


def test_second_review_updates_in_place(review_client):
    client, storage = review_client

    client.post("/userspace/submit_review", json=BODY)
    resp = client.post("/userspace/submit_review", json=BODY)

    # 1 -> 3 is the graduation (see GRADUATING_STEPS in srs.py); seeing the second
    # step here proves the call read the first review's state back rather than
    # starting over. The number moved when the ladder was shortened; what the
    # assertion is for did not.
    assert resp.json()["interval"] == 3
    docs = _docs(storage)
    assert len(docs) == 1
    assert docs[0]["reps"] == 2


def test_homographs_get_separate_schedules(review_client):
    """The whole reason the unique index includes `gloss`."""
    client, storage = review_client

    client.post("/userspace/submit_review", json=BODY)
    client.post("/userspace/submit_review", json={**BODY, "gloss": "to like"})

    assert sorted(d["gloss"] for d in _docs(storage)) == ["to like", "to love"]


def test_due_is_the_reviewers_local_midnight(review_client):
    """tz_offset uses getTimezoneOffset()'s sign: 420 is UTC-7, whose midnight
    is 07:00 UTC."""
    client, storage = review_client

    resp = client.post("/userspace/submit_review", json={**BODY, "tz_offset": 420})
    assert resp.json()["due"].endswith("T00:00:00-07:00")
    due = _docs(storage)[0]["due"]
    assert (due.hour, due.minute) == (7, 0)


def test_bad_rating_is_rejected(review_client):
    client, storage = review_client

    resp = client.post("/userspace/submit_review", json={**BODY, "rating": "perfect"})
    assert resp.status_code == 400
    assert _docs(storage) == []


def test_missing_uid_is_unauthorized(mdt):
    for name in ("routers.userspace", "routers.select"):
        sys.modules.pop(name, None)
    from routers import userspace
    from routers.firebase_auth import get_current_user_cookie

    app = FastAPI()
    app.include_router(userspace.router, prefix="/userspace")
    app.dependency_overrides[get_current_user_cookie] = lambda: {}

    resp = TestClient(app).post("/userspace/submit_review", json=BODY)
    assert resp.status_code == 401


def test_ensure_study_meta_is_idempotent_over_the_old_index(mdt, monkeypatch):
    """Re-running the migration on a collection still carrying the per-list
    index leaves exactly the two new indexes (plus Mongo's own _id_).

    Runs against a throwaway collection, not the real ``study_meta``: the test
    has to create the old index to have something to migrate, and doing that on
    a developer's live collection would drop their real indexes and fail on
    existing documents.
    """
    from pymongo import ASCENDING
    from utils import study_meta

    storage = mdt.atlas_client.get_database("App-Storage")
    scratch = "study_meta_migration_test"
    storage.drop_collection(scratch)
    storage.create_collection(scratch)
    storage[scratch].create_index(
        [("user_id", ASCENDING), ("language", ASCENDING),
         ("list_name", ASCENDING), ("lemma", ASCENDING)],
        unique=True, name="user_lang_list_lemma",
    )

    # Point ensure_study_meta() at the scratch collection by handing it a
    # database proxy whose `study_meta` attribute is that collection.
    class _Storage:
        def __init__(self, db):
            self._db = db
            self.study_meta = db[scratch]

        def list_collection_names(self):
            return self._db.list_collection_names()

        def create_collection(self, name):
            return self._db.create_collection(scratch)

    monkeypatch.setattr(
        study_meta.atlas_client, "get_database", lambda name: _Storage(storage)
    )
    try:
        study_meta.ensure_study_meta()
        study_meta.ensure_study_meta()
        names = set(storage[scratch].index_information())
        assert names == {"_id_", "user_lang_lemma_gloss", "user_lang_due"}
    finally:
        storage.drop_collection(scratch)
