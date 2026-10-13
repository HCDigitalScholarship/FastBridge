"""Unit tests for study_pairs() (utils/study_meta.py).

The function turns a saved list's stored word pairs into the (lemma, gloss)
keys that recall progress is filed under, so a disagreement between what gets
written and what gets read back shows up here rather than as silently missing
progress on the page.

utils/study_meta.py imports mongo_connection at module load, which builds a
MongoClient. study_pairs() never touches it, so it is stubbed at the test layer
(no production code changes) to keep this file off the network.
"""
import sys
from unittest.mock import MagicMock

sys.modules.setdefault("mongo_connection", MagicMock())

from utils.study_meta import study_pairs


def test_pairs_are_stripped_on_both_ends():
    """The client reads its gloss from a trimmed table cell, so an untrimmed
    stored definition has to land on the same key."""
    assert study_pairs([["amo", "  to love  "]]) == {("amo", "to love")}


def test_duplicate_entries_collapse():
    assert study_pairs([["amo", "to love"], ["amo", "to love"]]) == {("amo", "to love")}


def test_homographs_stay_separate():
    pairs = study_pairs([["amo", "to love"], ["amo", "to like"]])
    assert pairs == {("amo", "to love"), ("amo", "to like")}


def test_extra_columns_are_ignored():
    """Only the first two positions are the key; a longer row is still fine."""
    assert study_pairs([["amo", "to love", "Verb", 1]]) == {("amo", "to love")}


def test_one_malformed_entry_does_not_cost_the_rest():
    """A short, null or non-string pair is skipped on its own. The page wraps
    the whole lookup in a try/except, so raising here would drop recall
    progress for every word in the list, not just the broken one."""
    pairs = study_pairs([
        ["amo", "to love"],
        ["puella"],              # no gloss
        ["rex", None],           # null gloss
        [None, "nobody"],        # null lemma is still a usable key
        "notalist",              # a bare string indexes to characters
        ["video", "to see"],
    ])
    assert ("amo", "to love") in pairs
    assert ("video", "to see") in pairs
    assert ("puella", None) not in pairs
    assert ("rex", None) not in pairs


def test_empty_list_is_an_empty_set():
    assert study_pairs([]) == set()
