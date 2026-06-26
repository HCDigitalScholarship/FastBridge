"""Unit tests for the standalone functions in TextAnalyzer.py.

TextAnalyzer.py connects to MongoDB at import time (through MongoDefinitionTools) and pulls
in pandas/scipy/matplotlib/plotly. To test the two standalone functions
(find_hapax_legomena and round_decorator), we put fakes for those modules into sys.modules
before importing, so no Mongo connection happens and the heavy libraries don't load. No
production code changes.

The readability formulas (ari/lix/rix/spache/dale_chall) aren't tested here on purpose:
they read instance state (self.texts) instead of taking numbers as arguments, so there's
no clean way to test them without a refactor or an awkward fake analyzer. Left for later.
"""
import importlib
import sys
from unittest import mock

import pytest

# Modules imported at the top of TextAnalyzer.py that we don't want to really load.
# MongoDefinitionTools is the one that would otherwise connect to production Mongo.
_FAKE_MODULES = [
    "MongoDefinitionTools",
    "pandas", "seaborn", "numpy",
    "matplotlib", "matplotlib.pyplot", "matplotlib.font_manager",
    "plotly", "plotly.express",
    "scipy", "scipy.signal",
]

_TARGET = "TextAnalyzer"


@pytest.fixture(scope="module")
def text_analyzer():
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


# --- find_hapax_legomena ---------------------------------------------------
# Hapax legomena = lemmas that appear exactly once. The dictionary maps a wordform to a
# record with a 'SIMPLE_LEMMA'; several wordforms can share one lemma.

def test_find_hapax_returns_lemmas_seen_exactly_once(text_analyzer):
    dictionary = {
        "amo": {"SIMPLE_LEMMA": "amo"},
        "amas": {"SIMPLE_LEMMA": "amo"},   # same lemma as "amo" -> count 2
        "rex": {"SIMPLE_LEMMA": "rex"},     # count 1 -> hapax
    }
    words = ["amo", "amas", "rex"]
    assert text_analyzer.find_hapax_legomena(words, dictionary) == ["Rex"]


def test_find_hapax_preserves_first_seen_order(text_analyzer):
    dictionary = {
        "rex": {"SIMPLE_LEMMA": "rex"},
        "puella": {"SIMPLE_LEMMA": "puella"},
    }
    assert text_analyzer.find_hapax_legomena(["rex", "puella"], dictionary) == ["Rex", "Puella"]


def test_find_hapax_falls_back_to_uppercase_key(text_analyzer):
    # exact "amo" is absent, but its upper-cased form is a key
    dictionary = {"AMO": {"SIMPLE_LEMMA": "amo"}}
    assert text_analyzer.find_hapax_legomena(["amo"], dictionary) == ["Amo"]


def test_find_hapax_ignores_words_not_in_dictionary(text_analyzer):
    dictionary = {"rex": {"SIMPLE_LEMMA": "rex"}}
    assert text_analyzer.find_hapax_legomena(["rex", "xyzzy"], dictionary) == ["Rex"]


def test_find_hapax_skips_entries_with_falsy_value(text_analyzer):
    # present in the dict but with a falsy record -> contributes nothing
    dictionary = {"amo": None}
    assert text_analyzer.find_hapax_legomena(["amo"], dictionary) == []


# round decorator

def test_round_decorator_rounds_a_float(text_analyzer):
    @text_analyzer.round_decorator
    def f():
        return 3.14159
    assert f() == 3.14


def test_round_decorator_rounds_numbers_inside_a_tuple_only(text_analyzer):
    @text_analyzer.round_decorator
    def f():
        return (1.23456, "x", 2, 2.71828)
    assert f() == (1.23, "x", 2, 2.72)


def test_round_decorator_passes_through_strings(text_analyzer):
    @text_analyzer.round_decorator
    def f():
        return "hello"
    assert f() == "hello"


def test_round_decorator_does_not_round_lists(text_analyzer):
    # a list isn't a tuple, so it's returned untouched
    @text_analyzer.round_decorator
    def f():
        return [1.11111, 2.22222]
    assert f() == [1.11111, 2.22222]
