"""Unit tests for lemmatize() itself, on the dictionary ("morpheus") path.

lemmatize() does the main work of the lemmatizer: it walks the text, reads [1.2]-style
location markers, numbers poetry lines, cleans each word, and looks up its lemma. These
tests cover only the dictionary path (format="MORPHEUS"), which never loads Stanza or CLTK.

Same idea as test_lemmatize.py: fake the heavy imports before importing the module. On top
of that we inject a fake `{language}_morpheus_conversion` module so we control the lookup
output. No production code changes, and nothing reaches the network.
"""
import importlib
import re
import sys
import types
from unittest import mock

import pytest

# Heavy / framework modules imported at the top of lemmatize.py.
_FAKE_MODULES = [
    "stanza",
    "cltk", "cltk.lemmatize", "cltk.lemmatize.lat", "cltk.lemmatize.grc",
    "cltk.utils", "cltk.data", "cltk.data.fetch",
    "fastapi", "fastapi.templating",
    "starlette", "starlette.responses",
]

_TARGET = "routers.ToolsApp.lemmatize"

# The exact marker regex the route compiles (see lemmatizing_handler in lemmatize.py).
MARKER_RE = re.compile(r'\[[0-9]+(\_|\.?[0-9]+)*\]')

HEADER = "TITLE,LOCATION,SECTION,RUNNINGCOUNT,TEXT"


@pytest.fixture(scope="module")
def lemmatize_mod():
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


@pytest.fixture
def run_lemmatize(lemmatize_mod):
    """Call lemmatize() with a controllable fake conversion dict and return the CSV text.

    Injects a fake routers.ToolsApp.<language>_morpheus_conversion module (so the real data
    file is never loaded) and restores sys.modules afterwards.
    """
    def _run(text, *, language="Latin", lemma_lex=None, conversion=None,
             fmt="MORPHEUS", poetry=False, location=""):
        modname = f"routers.ToolsApp.{language}_morpheus_conversion"
        fake = types.ModuleType(modname)
        fake.conversion_dict = conversion or {}
        saved = sys.modules.get(modname)
        sys.modules[modname] = fake
        try:
            return lemmatize_mod.lemmatize(
                text, location, MARKER_RE, language, lemma_lex or {}, fmt, poetry
            )
        finally:
            if saved is None:
                sys.modules.pop(modname, None)
            else:
                sys.modules[modname] = saved
    return _run


def test_dictionary_hit_and_miss(run_lemmatize):
    out = run_lemmatize("amo ignotum", lemma_lex={"amo": "amo"})
    assert out == (
        f"{HEADER}\n"
        "morpheus: amo,,0,1,amo\n"
        "morpheus: NONE,,0,2,ignotum\n"
    )


def test_conversion_dict_overrides_morpheus_prefix(run_lemmatize):
    out = run_lemmatize("amo", lemma_lex={"amo": "amo"}, conversion={"amo": "amare"})
    assert out == f"{HEADER}\namare,,0,1,amo\n"


def test_location_markers_set_location_and_section(run_lemmatize):
    out = run_lemmatize("[1] amo [2] puella", lemma_lex={"amo": "amo", "puella": "puella"})
    assert out == (
        f"{HEADER}\n"
        "morpheus: amo,1,1,1,amo\n"
        "morpheus: puella,2,2,2,puella\n"
    )


def test_marker_attached_to_word_is_stripped_but_text_keeps_original(run_lemmatize):
    # "[1]amo" -> marker stripped before lookup, but the TEXT column keeps the raw token
    out = run_lemmatize("[1]amo", lemma_lex={"amo": "amo"})
    assert out == f"{HEADER}\nmorpheus: amo,1,1,1,[1]amo\n"


def test_poetry_mode_numbers_each_line(run_lemmatize):
    out = run_lemmatize(
        "amo\npuella",
        lemma_lex={"amo": "amo", "puella": "puella"},
        poetry=True,
    )
    assert out == (
        f"{HEADER}\n"
        "morpheus: amo,1,1,1,amo\n"
        "morpheus: puella,2,2,2,puella\n"
    )


def test_running_count_increments_per_emitted_row(run_lemmatize):
    out = run_lemmatize("amo amo amo", lemma_lex={"amo": "amo"})
    assert out == (
        f"{HEADER}\n"
        "morpheus: amo,,0,1,amo\n"
        "morpheus: amo,,0,2,amo\n"
        "morpheus: amo,,0,3,amo\n"
    )


def test_greek_preserves_accents_for_lookup(run_lemmatize):
    # The Greek branch only runs depunctuate() (no strip_accents/lower), so it looks up
    # the accented form. A Latin run would strip it to "λογος" and miss this key.
    out = run_lemmatize("λόγος", language="Greek", lemma_lex={"λόγος": "logos"})
    assert out == f"{HEADER}\nmorpheus: logos,,0,1,λόγος\n"
