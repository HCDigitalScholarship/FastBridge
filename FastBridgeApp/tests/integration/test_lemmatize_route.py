"""Integration test for the lemmatizer HTTP route (POST /lemmatizer/).

This drives the real FastAPI route end to end with an in-process TestClient, rather than
calling lemmatize() directly. To keep it test-only and offline we:
  - mount only the lemmatize router on a throwaway app, so main, Mongo and Firebase are
    never imported,
  - fake Stanza/CLTK before import (the dictionary path doesn't use them),
  - and monkeypatch tempfile so the route's hardcoded /tmp directory doesn't break the test
    on a machine without /tmp.

It uses the real Latin_lemmata and Latin_morpheus_conversion data, so the assertions are
structural (the CSV shape and the TEXT column) rather than tied to specific lemma values.
"""
import importlib
import sys
import tempfile
from unittest import mock

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi import FastAPI
from fastapi.testclient import TestClient

_FAKE_MODULES = [
    "stanza",
    "cltk", "cltk.lemmatize", "cltk.lemmatize.lat", "cltk.lemmatize.grc",
    "cltk.utils", "cltk.data", "cltk.data.fetch",
]
_LEMMATIZE = "routers.ToolsApp.lemmatize"


@pytest.fixture(scope="module")
def client():
    saved = {name: sys.modules.get(name) for name in _FAKE_MODULES + [_LEMMATIZE]}
    for name in _FAKE_MODULES:
        sys.modules[name] = mock.MagicMock()
    sys.modules.pop(_LEMMATIZE, None)
    try:
        lemmatize = importlib.import_module(_LEMMATIZE)
        app = FastAPI()
        app.include_router(lemmatize.router, prefix="/lemmatizer")
        yield TestClient(app)
    finally:
        for name, original in saved.items():
            if original is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original


@pytest.fixture(autouse=True)
def tmp_file_anywhere(monkeypatch):
    # The route hardcodes dir="/tmp" for its temp CSV, which doesn't exist on Windows.
    # Drop that kwarg so the test runs on any platform. Production code is untouched.
    real_named_temp = tempfile.NamedTemporaryFile

    def named_temp_anywhere(*args, **kwargs):
        kwargs.pop("dir", None)
        return real_named_temp(*args, **kwargs)

    monkeypatch.setattr(tempfile, "NamedTemporaryFile", named_temp_anywhere)


def test_post_returns_lemmatized_csv(client):
    resp = client.post(
        "/lemmatizer/",
        data={
            "format": "MORPHEUS",
            "language": "Latin",
            "poetry": "No",
            "resulting_filename": "sheet",
            "text": "amo puella",
        },
        files={"file": ("empty.txt", b"", "text/plain")},
    )

    assert resp.status_code == 200
    assert "sheet.csv" in resp.headers.get("content-disposition", "")

    body = resp.content.decode("utf-8-sig")  # the route prepends a BOM
    lines = [line for line in body.splitlines() if line]
    assert lines[0] == "TITLE,LOCATION,SECTION,RUNNINGCOUNT,TEXT"
    assert len(lines) == 3                       # header + one row per input word
    assert lines[1].endswith(",amo")
    assert lines[2].endswith(",puella")
