"""Integration tests for the include/exclude word filters.

The select page lets you refine a vocabulary selection by another text: "include" keeps only
words shared with the other text, "exclude" drops them. That word-removal is *intended*, so
these tests pin the intended kept/removed sets down. They run the real corpus pipeline
(mg_get_locations -> mg_get_text_as_Text -> Text.get_words) against the seeded fixture, which
is the expensive, bug-prone part; the set algebra itself mirrors what the /result route does.

They skip automatically when no local Mongo is reachable (see conftest.py).
"""


def _headword_set(mdt, title):
    linked, word_count = mdt.mg_get_locations("Latin", title, get_index=True)
    book = mdt.mg_get_text_as_Text("Latin", title, linked, word_count)
    return {word[0] for word in book.get_words("start", "end")}


def test_selection_returns_all_headwords(mdt, filter_texts):
    assert _headword_set(mdt, "Filter Text A") == {"AMO", "AMAS", "PUELLA", "REX"}
    assert _headword_set(mdt, "Filter Text B") == {"PUELLA", "REX", "LUNA"}


def test_include_keeps_only_shared_words(mdt, filter_texts):
    a = _headword_set(mdt, "Filter Text A")
    b = _headword_set(mdt, "Filter Text B")
    assert a & b == {"PUELLA", "REX"}


def test_exclude_removes_shared_words(mdt, filter_texts):
    a = _headword_set(mdt, "Filter Text A")
    b = _headword_set(mdt, "Filter Text B")
    # PUELLA/REX are shared, so excluding B by design drops them; AMO/AMAS remain.
    assert a - b == {"AMO", "AMAS"}
