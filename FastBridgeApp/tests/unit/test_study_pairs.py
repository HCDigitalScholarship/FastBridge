"""Unit tests for study_pairs() (utils/study_meta.py).

The function turns a saved list's stored word pairs into the (lemma, gloss) keys that recall
progress is filed under, so a disagreement between what gets written and what gets read back
shows up here rather than as silently missing progress on the page.

study_meta.py imports pymongo and mongo_connection at the top of the file, and the unit job
installs neither (see .github/workflows/tests.yml: unit tests get requirements-dev.txt only,
no database libraries). study_pairs() touches none of it, so each module is swapped for a
MagicMock before the import, the same way test_lemmatize.py handles Stanza and CLTK. The
real libraries never load and no production code changes.
"""
import importlib
import sys
from unittest import mock

import pytest

_FAKE_MODULES = ["pymongo", "pymongo.errors", "mongo_connection"]
_TARGET = "utils.study_meta"


@pytest.fixture(scope="module")
def study_pairs():
    saved = {name: sys.modules.get(name) for name in _FAKE_MODULES + [_TARGET]}
    for name in _FAKE_MODULES:
        sys.modules[name] = mock.MagicMock()
    sys.modules.pop(_TARGET, None)
    try:
        yield importlib.import_module(_TARGET).study_pairs
    finally:
        for name, original in saved.items():
            if original is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original


def test_pairs_are_stripped_on_both_ends(study_pairs):
    """The client reads its gloss from a trimmed table cell, so an untrimmed
    stored definition has to land on the same key."""
    assert study_pairs([["amo", "  to love  "]]) == {("amo", "to love")}


def test_duplicate_entries_collapse(study_pairs):
    assert study_pairs([["amo", "to love"], ["amo", "to love"]]) == {("amo", "to love")}


def test_homographs_stay_separate(study_pairs):
    pairs = study_pairs([["amo", "to love"], ["amo", "to like"]])
    assert pairs == {("amo", "to love"), ("amo", "to like")}


def test_extra_columns_are_ignored(study_pairs):
    """Only the first two positions are the key; a longer row is still fine."""
    assert study_pairs([["amo", "to love", "Verb", 1]]) == {("amo", "to love")}


def test_one_malformed_entry_does_not_cost_the_rest(study_pairs):
    """A short or non-string pair is skipped on its own. The page wraps the whole
    lookup in a try/except, so raising here would drop recall progress for every
    word in the list, not just the broken one."""
    pairs = study_pairs([
        ["amo", "to love"],
        ["puella"],              # no gloss
        ["rex", None],           # null gloss
        ["video", "to see"],
    ])
    assert ("amo", "to love") in pairs
    assert ("video", "to see") in pairs
    assert ("puella", None) not in pairs
    assert ("rex", None) not in pairs


def test_empty_list_is_an_empty_set(study_pairs):
    assert study_pairs([]) == set()
