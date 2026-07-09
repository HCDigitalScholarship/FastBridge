"""Unit tests for the readability formulas in TextAnalyzer.py
(spache, dale_chall, ari, lix, rix).

These are methods on TextAnalyzer that read instance state (self.texts) and pull word data
through get_slice or _flatten_texts, so they can't be called as plain functions. To test
the formula math without changing any production code, we build an analyzer with __new__
(which skips the Mongo-loading __init__), set only the attributes each method reads, and
feed known word lists through the get_slice / _flatten_texts seam. Nothing connects to a
database or the network.

Word tuples carry the fields these methods look at: index 0 is the lemma, index 2 is the
orthographic form, and index 7 is the section (used as the sentence boundary).
"""
import importlib
import sys
from unittest import mock

import pytest

# Same heavy imports we fake in test_text_analyzer.py. MongoDefinitionTools is the one that
# would otherwise open a database connection at import time.
_FAKE_MODULES = [
    "MongoDefinitionTools",
    "pandas", "seaborn", "numpy",
    "matplotlib", "matplotlib.pyplot", "matplotlib.font_manager",
    "plotly", "plotly.express",
    "scipy", "scipy.signal",
]

_TARGET = "TextAnalyzer"


@pytest.fixture(scope="module")
def ta_module():
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


def word(lemma="", orth="", section="1"):
    """A word tuple with just the fields the readability methods read."""
    return (lemma, "", orth, "", "", "", "", section)


def new_analyzer(ta_module):
    # Skip __init__ (it would load the Mongo dictionary); we set the few attributes each
    # formula actually reads.
    return ta_module.TextAnalyzer.__new__(ta_module.TextAnalyzer)


# These four words span two sections, with two of them unfamiliar (not in dcc). The
# numbers below are worked out from that.
LATIN_WORDS = [
    word("amo", section="1"),
    word("rex", section="1"),
    word("puella", section="2"),
    word("vita", section="2"),
]

# orthographic forms chosen so exactly two are "long" (more than 6 letters).
ORTH_WORDS = [
    word(orth="amo", section="1"),        # 3 letters
    word(orth="elephant", section="1"),   # 8 letters -> long
    word(orth="puella", section="2"),     # 6 letters
    word(orth="magnitudo", section="2"),  # 9 letters -> long
]


def test_ari_score(ta_module, monkeypatch):
    a = new_analyzer(ta_module)
    a.texts = [(None, None, None)]
    monkeypatch.setattr(ta_module, "get_slice", lambda *args, **kwargs: LATIN_WORDS)
    # 16 chars / 4 words, 4 words / 2 sentences -> 4.71*4 + 0.5*2 - 21.43
    assert a.ari_score() == -1.59


def test_spache_score(ta_module, monkeypatch):
    a = new_analyzer(ta_module)
    a.texts = [(None, None, None)]
    a.dcc = {"amo", "rex"}
    monkeypatch.setattr(ta_module, "get_slice", lambda *args, **kwargs: LATIN_WORDS)
    # avg sentence length 2, 50% unfamiliar -> 0.121*2 + 0.082*50 + 0.659
    assert a.spache_score() == 5.0


def test_dale_chall_score(ta_module, monkeypatch):
    a = new_analyzer(ta_module)
    a.texts = [(None, None, None)]
    a.dcc = {"amo", "rex"}
    monkeypatch.setattr(ta_module, "get_slice", lambda *args, **kwargs: LATIN_WORDS)
    # 50% difficult, sentence length 2; returns (classic score, new variant)
    assert a.dale_chall_score() == (11.63, 15.12)


def test_lix_score(ta_module):
    a = new_analyzer(ta_module)
    a.texts = [object()]
    a._flatten_texts = lambda: ORTH_WORDS
    # 2 words per sentence + 50% long words
    assert a.lix_score() == 52.0


def test_rix_score(ta_module):
    a = new_analyzer(ta_module)
    a.texts = [object()]
    a._flatten_texts = lambda: ORTH_WORDS
    # 2 long words / 2 sentences
    assert a.rix_score() == 1.0


def test_ari_score_returns_na_without_texts(ta_module):
    a = new_analyzer(ta_module)
    a.texts = []
    assert a.ari_score() == "NA"


def test_lix_score_returns_na_with_a_single_section(ta_module):
    a = new_analyzer(ta_module)
    a.texts = [object()]
    a._flatten_texts = lambda: [word(orth="amo", section="1"), word(orth="rex", section="1")]
    assert a.lix_score() == "NA"


def test_dale_chall_returns_na_pair_without_texts(ta_module):
    a = new_analyzer(ta_module)
    a.texts = []
    assert a.dale_chall_score() == ("NA", "NA")
