"""Unit tests for the small string helpers in routers/ToolsApp/lemmatize.py.
lemmatize.py imports Stanza, CLTK and FastAPI at the top of the file, so a unit test can't
import it the normal way. Instead we put fake versions of those modules into sys.modules
before importing it (see the `lemmatize` fixture). The heavy libraries never load, and no
production code changes.
"""
import importlib
import sys
from unittest import mock

import pytest

# Heavy third-party / framework modules imported at the top of lemmatize.py. We don't want
# the real ones loading in a unit test, so each is swapped for a MagicMock before the import.
# NOTE: the dotted submodules (fastapi.responses, starlette.concurrency, ...) must be listed
# individually — a mocked parent package is NOT a real package, so `from fastapi.responses
# import JSONResponse` only resolves if "fastapi.responses" is itself in sys.modules.
_FAKE_MODULES = [
    "stanza",
    "cltk", "cltk.lemmatize", "cltk.lemmatize.lat", "cltk.lemmatize.grc",
    "cltk.utils", "cltk.data", "cltk.data.fetch",
    "fastapi", "fastapi.templating", "fastapi.responses",
    "starlette", "starlette.responses", "starlette.concurrency",
]
_TARGET = "routers.ToolsApp.lemmatize"


@pytest.fixture(scope="module")
def lemmatize():
    saved = {name: sys.modules.get(name) for name in _FAKE_MODULES + [_TARGET]}
    for name in _FAKE_MODULES:
        sys.modules[name] = mock.MagicMock()
    sys.modules.pop(_TARGET, None)
    try:
        yield importlib.import_module(_TARGET)
    finally:
        for name, original in saved.items():
            if original is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original


# strip accents
def test_strip_accents_removes_latin_diacritics(lemmatize):
    assert lemmatize.strip_accents("café") == "cafe"
    assert lemmatize.strip_accents("āēīōū") == "aeiou"


def test_strip_accents_removes_greek_diacritics(lemmatize):
    assert lemmatize.strip_accents("λόγος") == "λογος"


def test_strip_accents_leaves_plain_text_unchanged(lemmatize):
    assert lemmatize.strip_accents("Ovid") == "Ovid"
    assert lemmatize.strip_accents("") == ""


# remove punctuation
def test_depunctuate_removes_punctuation_keeps_spaces(lemmatize):
    assert lemmatize.depunctuate("hello, world!") == "hello world"


def test_depunctuate_strips_apostrophes_and_periods(lemmatize):
    assert lemmatize.depunctuate("a.b,c;d") == "abcd"
    assert lemmatize.depunctuate("rex's") == "rexs"


def test_depunctuate_leaves_accented_letters_and_digits(lemmatize):
    # only punctuation is removed; accented letters and digits survive
    assert lemmatize.depunctuate("café!") == "café"
    assert lemmatize.depunctuate("1, 2, 3") == "1 2 3"