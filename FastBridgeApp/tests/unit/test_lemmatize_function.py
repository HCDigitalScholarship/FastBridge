"""Unit tests for lemmatize() itself, on the dictionary ("morpheus") path.
lemmatize() walks the text, reads [1.2]-style location markers, numbers poetry lines,
cleans each word, looks up its lemma, and crosswalks that lemma to its Bridge dictionary
Head Word. These tests cover only the dictionary path (format="MORPHEUS"), which never
loads Stanza or CLTK.

Same idea as test_lemmatize.py: fake the heavy imports before importing the module. On top
of that we inject a fake `{language}_morpheus_conversion` module so we control the
lemma->Head Word crosswalk. No production code changes, and nothing reaches the network.

CSV columns match the Bridge ontology:
    Head Word, Location, Section, Counter, Orthographic Form, Crosswalk
where Head Word is the lemma crosswalked through conversion_dict, Orthographic Form is the
original word, and Crosswalk is "FAILED" when a resolved lemma had no Bridge Head Word.
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
    "fastapi", "fastapi.templating", "fastapi.responses",
    "starlette", "starlette.responses", "starlette.concurrency",
]
_TARGET = "routers.ToolsApp.lemmatize"

# The exact marker regex the route compiles (see lemmatizing_handler in lemmatize.py).
MARKER_RE = re.compile(r'\[[0-9]+(\_|\.?[0-9]+)*\]')
HEADER = "Head Word,Location,Section,Counter,Orthographic Form,Crosswalk"


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
    out = run_lemmatize("amo ignotum", lemma_lex={"amo": "amo"},
                        conversion={"amo": "AMO"})
    assert out == (
        f"{HEADER}\n"
        "AMO,,0,1,amo,\n"          # resolved + crosswalked to the Bridge Head Word
        "NONE,,0,2,ignotum,\n"     # not in the lexicon -> NONE
    )


def test_crosswalk_maps_lemma_to_head_word(run_lemmatize):
    out = run_lemmatize("amo", lemma_lex={"amo": "amo"}, conversion={"amo": "AMO"})
    assert out == f"{HEADER}\nAMO,,0,1,amo,\n"


def test_crosswalk_failure_is_flagged(run_lemmatize):
    # Lemma resolves, but it has no Bridge Head Word in the (empty) conversion table:
    # keep the raw lemma in Head Word and flag the row for a manual headword.
    out = run_lemmatize("amo", lemma_lex={"amo": "amo"}, conversion={})
    assert out == f"{HEADER}\namo,,0,1,amo,FAILED\n"


def test_location_markers_set_location_and_section(run_lemmatize):
    out = run_lemmatize("[1] amo [2] puella",
                        lemma_lex={"amo": "amo", "puella": "puella"},
                        conversion={"amo": "AMO", "puella": "PVELLA"})
    assert out == (
        f"{HEADER}\n"
        "AMO,1,1,1,amo,\n"
        "PVELLA,2,2,2,puella,\n"
    )


def test_marker_attached_to_word_is_stripped_but_form_keeps_original(run_lemmatize):
    # "[1]amo" -> marker stripped before lookup, but Orthographic Form keeps the raw token
    out = run_lemmatize("[1]amo", lemma_lex={"amo": "amo"}, conversion={"amo": "AMO"})
    assert out == f"{HEADER}\nAMO,1,1,1,[1]amo,\n"


def test_poetry_mode_numbers_each_line(run_lemmatize):
    out = run_lemmatize(
        "amo\npuella",
        lemma_lex={"amo": "amo", "puella": "puella"},
        conversion={"amo": "AMO", "puella": "PVELLA"},
        poetry=True,
    )
    assert out == (
        f"{HEADER}\n"
        "AMO,1,1,1,amo,\n"
        "PVELLA,2,2,2,puella,\n"
    )


def test_counter_increments_per_emitted_row(run_lemmatize):
    out = run_lemmatize("amo amo amo", lemma_lex={"amo": "amo"},
                        conversion={"amo": "AMO"})
    assert out == (
        f"{HEADER}\n"
        "AMO,,0,1,amo,\n"
        "AMO,,0,2,amo,\n"
        "AMO,,0,3,amo,\n"
    )


def test_greek_preserves_accents_for_lookup(run_lemmatize):
    # The Greek branch only runs depunctuate() (no strip_accents/lower), so it looks up
    # the accented form. A Latin run would strip it to "λογος" and miss this key.
    out = run_lemmatize("λόγος", language="Greek", lemma_lex={"λόγος": "logos"},
                        conversion={"logos": "LOGOS"})
    assert out == f"{HEADER}\nLOGOS,,0,1,λόγος,\n"
