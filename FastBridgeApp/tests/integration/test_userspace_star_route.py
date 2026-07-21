"""Route-level test for per-user star toggling (POST /userspace/toggle_star).

Drives the real userspace router with an in-process TestClient against a local Mongo, so it
covers the endpoint wiring - request -> $addToSet/$pull on the *caller's* lists doc - rather
than the query in isolation. Auth is overridden to a fixed test user, and firebase_admin is
stubbed so the router imports without a service-account cert (mirrors the e2e harness). Skips
when no local Mongo is reachable, via the shared `mdt` fixture.
"""
import sys
from unittest.mock import MagicMock

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

# userspace.py does `from firebase_admin import auth` at import
# stub it so the router loads without Firebase credentials. setdefault leaves a real module in place if one already exists
sys.modules.setdefault("firebase_admin", MagicMock())

from fastapi import FastAPI
from fastapi.testclient import TestClient

TEST_UID = "star-route-test-user"


@pytest.fixture
def userspace_client(mdt):
    # `mdt` has bound mongo_connection to the local Mongo; import the router fresh so it picks
    # up that binding rather than a stale (or Atlas-pointed) module from an earlier test
    for name in ("routers.userspace", "routers.select"):
        sys.modules.pop(name, None)
    from routers import userspace
    from routers.firebase_auth import get_current_user_cookie

    app = FastAPI()
    app.include_router(userspace.router, prefix="/userspace")
    app.dependency_overrides[get_current_user_cookie] = lambda: {"uid": TEST_UID}

    storage = userspace.atlas_client.get_database("App-Storage")
    storage.lists.delete_many({"user_id": TEST_UID})
    yield TestClient(app), storage
    storage.lists.delete_many({"user_id": TEST_UID})


def _stars(storage):
    doc = storage.lists.find_one({"user_id": TEST_UID}, {"starred": 1, "_id": 0}) or {}
    return doc.get("starred", [])


def test_star_then_unstar_round_trips(userspace_client):
    client, storage = userspace_client
    body = {
        "owner_id": "owner-1", "language": "Latin", "list_name": "My List",
        "word": ["amo", "to love"], "starred": True,
    }

    resp = client.post("/userspace/toggle_star", json=body)
    assert resp.status_code == 200
    assert resp.json()["starred"] is True
    assert _stars(storage) == [
        {"owner_id": "owner-1", "language": "Latin", "list_name": "My List", "word": ["amo", "to love"]}
    ]

    # re-starring the same word doesn't duplicate
    client.post("/userspace/toggle_star", json=body)
    assert len(_stars(storage)) == 1

    # Unstar pulls exactly that record back out
    resp = client.post("/userspace/toggle_star", json={**body, "starred": False})
    assert resp.status_code == 200
    assert resp.json()["starred"] is False
    assert _stars(storage) == []


def test_stars_are_scoped_per_list(userspace_client):
    client, storage = userspace_client
    client.post("/userspace/toggle_star", json={
        "owner_id": "owner-1", "language": "Latin", "list_name": "List A",
        "word": ["amo", "to love"], "starred": True})
    client.post("/userspace/toggle_star", json={
        "owner_id": "owner-1", "language": "Latin", "list_name": "List B",
        "word": ["rex", "king"], "starred": True})

    stars = _stars(storage)
    assert len(stars) == 2
    # Unstarring one list's word leaves the other list's star intact
    client.post("/userspace/toggle_star", json={
        "owner_id": "owner-1", "language": "Latin", "list_name": "List A",
        "word": ["amo", "to love"], "starred": False})
    remaining = _stars(storage)
    assert remaining == [
        {"owner_id": "owner-1", "language": "Latin", "list_name": "List B", "word": ["rex", "king"]}
    ]


def test_empty_word_is_rejected(userspace_client):
    client, _ = userspace_client
    resp = client.post("/userspace/toggle_star", json={
        "owner_id": "owner-1", "language": "Latin", "list_name": "My List",
        "word": [], "starred": True})
    assert resp.status_code == 400
