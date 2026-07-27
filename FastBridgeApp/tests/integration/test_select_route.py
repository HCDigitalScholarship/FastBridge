"""Route-level test for the corpus section-loading endpoint (GET /select/sections/...).

This drives the real select router with an in-process TestClient, so it covers the wiring
layer (route -> query function -> JSON) rather than just the query function in isolation --
the layer where "loading a list search from the corpus wouldn't work" most plausibly lives.

It mounts only the select router on a throwaway app, so main/Firebase are never imported, and
it seeds a local Mongo via the shared `seeded` fixture. Skips when no local Mongo is reachable.
"""
import sys

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def select_client(mdt, seeded, monkeypatch):
    # Re-import the router after `mdt` has bound MongoDefinitionTools to the local Mongo, so
    # the route's query functions talk to the seeded fixture DB rather than a stale module.
    sys.modules.pop("routers.select", None)
    from routers import select

    # select_section tries mg_get_sections (a Static-JSON lookup) first and only falls back to
    # the Mongo corpus load on failure. Force the fallback so the test exercises the corpus
    # path (route -> mg_get_locations) deterministically, independent of any Static files.
    def _force_fallback(*args, **kwargs):
        raise RuntimeError("force corpus fallback")

    monkeypatch.setattr(select, "mg_get_sections", _force_fallback)

    app = FastAPI()
    app.include_router(select.router, prefix="/select")
    return TestClient(app)


def test_select_section_loads_corpus_linked_list(select_client):
    resp = select_client.get("/select/sections/Fixture Text/Latin/")
    assert resp.status_code == 200
    assert resp.json() == {
        "start": "start",
        "1.1": "start",
        "1.2": "1.1",
        "end": "1.2",
    }
