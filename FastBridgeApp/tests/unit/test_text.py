"""Unit tests for the section and word selection logic in text.py.

text.py has no imports, so nothing here touches a database, the network, or any heavy
dependency. These tests pin down the behavior the code actually has, including a few
surprising edges noted below, so a later change can't break it without a test going red.
"""
import pytest

from text import Text, next_section


# next section

def test_next_section_increments_plain_number():
    assert next_section("1") == "2"
    assert next_section("9") == "10"
    assert next_section("58") == "59"


def test_next_section_uses_only_first_dotted_component():
    # It increments the first component and drops the rest, so "1.1" gives "2", not
    # "2.1". Pinned here so the behavior stays deliberate.
    assert next_section("1.1") == "2"
    assert next_section("2.3.4") == "3"


def test_next_section_increments_trailing_letter():
    assert next_section("2b") == "2c"
    assert next_section("58B") == "58C"


def test_next_section_lettered_with_dotted_suffix():
    assert next_section("2b.1") == "2c"



# Text.get_section(range_start, range_end)

#
# Data model (as used by the app):
#   sections[key]            -> index of the LAST word of that section (0-based);
#                               the "start" sentinel sits just before the first word.
#   section_linkedlist[key]  -> the section that PRECEDES `key`.
# A section therefore spans from (last index of its predecessor)+1 .. (its own last
# index)+1, expressed as a Python [start, end) slice.

def make_text(words, sections, linked, name="OvidMet"):
    return Text(
        name=name,
        sections=sections,
        words=words,
        section_linkedlist=linked,
        subsections=1,
        language="Latin",
    )


@pytest.fixture
def sample_text():
    words = [
        ("amo", "L1"),     # 0
        ("amas", "L1"),    # 1
        ("amat", "L2"),    # 2
        ("amamus", "L2"),  # 3
        ("amatis", "L3"),  # 4
        ("amant", "L3"),   # 5
    ]
    sections = {"start": -1, "1": 1, "2": 3, "3": 5, "end": 5}
    linked = {"start": "start", "1": "start", "2": "1", "3": "2", "end": "3"}
    return make_text(words, sections, linked)


def test_get_section_first_section(sample_text):
    # predecessor of "1" is "start" (index -1) -> start = 0; end = sections["1"]+1 = 2
    assert sample_text.get_section("1", "1") == (0, 2)


def test_get_section_middle_section(sample_text):
    # predecessor of "2" is "1" (index 1) -> start = 2; end = sections["2"]+1 = 4
    assert sample_text.get_section("2", "2") == (2, 4)


def test_get_section_spanning_range(sample_text):
    assert sample_text.get_section("1", "3") == (0, 6)


def test_get_section_to_end_keyword(sample_text):
    assert sample_text.get_section("2", "end") == (2, 6)


def test_get_section_invalid_start_raises(sample_text):
    with pytest.raises(ValueError, match="Invalid start section"):
        sample_text.get_section("99", "1")


def test_get_section_invalid_end_raises(sample_text):
    with pytest.raises(ValueError, match="Invalid end section"):
        sample_text.get_section("1", "99")


def test_get_section_predecessor_index_zero_is_not_incremented():
    # Covers the `if start_idx != 0` branch: when the predecessor's last index is 0,
    # the +1 is skipped and the section starts at index 0.
    words = [("a", "x"), ("b", "x"), ("c", "x")]
    sections = {"start": -1, "1": 0, "2": 2, "end": 2}
    linked = {"start": "start", "1": "start", "2": "1", "end": "2"}
    text = make_text(words, sections, linked)
    assert text.get_section("2", "2") == (0, 3)

# Text.get_words(user_start, user_end, stats=False, oracle=False)

def test_get_words_default_appends_source_text_name(sample_text):
    # default (select) mode appends the text name to each word tuple
    assert sample_text.get_words("1", "1") == [
        ("amo", "L1", "OvidMet"),
        ("amas", "L1", "OvidMet"),
    ]


def test_get_words_stats_mode_keeps_raw_tuples(sample_text):
    # stats mode returns the raw word tuples, without the source-text name
    assert sample_text.get_words("1", "1", stats=True) == [
        ("amo", "L1"),
        ("amas", "L1"),
    ]


def test_get_words_oracle_mode_returns_wordforms_only(sample_text):
    assert sample_text.get_words("1", "1", oracle=True) == ["amo", "amas"]


def test_get_words_oracle_takes_precedence_over_stats(sample_text):
    # oracle is checked first, so stats is ignored when both are set
    assert sample_text.get_words("1", "1", stats=True, oracle=True) == ["amo", "amas"]


def test_get_words_end_sentinel_falls_back_to_full_length():
    # Covers the `if end == -1` branch: when sections["end"] is -2, get_section yields
    # end == -1 and get_words substitutes len(words).
    words = [("a", "x"), ("b", "x"), ("c", "x"), ("d", "x")]
    sections = {"start": -1, "1": 1, "end": -2}
    linked = {"start": "start", "1": "start", "end": "1"}
    text = make_text(words, sections, linked, name="T")
    assert text.get_words("1", "end") == [
        ("a", "x", "T"),
        ("b", "x", "T"),
        ("c", "x", "T"),
        ("d", "x", "T"),
    ]
