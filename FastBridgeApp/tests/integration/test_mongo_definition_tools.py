"""Integration tests for the MongoDefinitionTools query functions.

These run against a real (local, temporary) MongoDB seeded by the `seeded` fixture in
conftest.py, so they exercise the actual database queries rather than mocked data. They
skip automatically when no local Mongo is reachable.
"""
import pytest


def test_get_field_subset_returns_the_requested_columns(mdt, seeded):
    result = mdt.get_field_subset(["head_word", "orthographic_form"], "fixture_text")
    assert set(result["head_word"]) == {"AMO", "AMAS", "PUELLA", "REX"}
    assert set(result["orthographic_form"]) == {"amo", "amas", "puella", "rex"}


def test_build_dict_structure_maps_each_title_to_its_fields(mdt, seeded):
    result = mdt.build_dict_structure("fixture_dict")
    assert result["amo"] == ("amo", "to love")
    assert result["puella"] == ("puella", "girl")


def test_mg_get_locations_builds_linked_list_and_index(mdt, seeded):
    linked, word_count = mdt.mg_get_locations("Latin", "Fixture Text", get_index=True)
    # locations collapse repeats and link each section back to the previous one
    assert linked == {"start": "start", "1.1": "start", "1.2": "1.1", "end": "1.2"}
    # word_count records the last running index seen at each location
    assert word_count == {"start": 0, "end": -2, "1.1": 1, "1.2": 3}


# --- messy-corpus coverage (the clean 4-row fixture gives false confidence) ----------------

def test_mg_get_locations_survives_messy_data(mdt, messy_seeded):
    # A null location and a missing section must not crash or invent a section, and the
    # duplicated consecutive location must still collapse to one entry.
    linked, word_count = mdt.mg_get_locations("Latin", "Messy Text", get_index=True)
    assert linked == {"start": "start", "1.1": "start", "1.2": "1.1", "end": "1.2"}
    # the null-location document contributes no bogus key
    assert set(word_count) == {"start", "end", "1.1", "1.2"}


def test_mg_get_locations_handles_empty_corpus(mdt, messy_seeded):
    # A text whose collection has no documents should degrade to just start/end, not blow up.
    linked = mdt.mg_get_locations("Latin", "Empty Text", get_index=False)
    assert linked == {"start": "start", "end": "start"}


@pytest.mark.xfail(
    reason="prod bug: mg_get_locations uses its local `key` before assignment when the first "
           "document (by counter) has a null location, so get_index raises UnboundLocalError. "
           "When the function is fixed this flips to XPASS (strict) as a reminder to drop this.",
    raises=NameError,  # UnboundLocalError is a subclass of NameError
    strict=True,
)
def test_mg_get_locations_leading_null_location_crashes(mdt, leading_null_seeded):
    # Documents the case messy_seeded can't reach: a leading null location leaves `key`
    # unbound at `text_word_count[key] = local_index`.
    mdt.mg_get_locations("Latin", "Leading Null Text", get_index=True)


def test_get_field_subset_only_returns_present_fields(mdt, messy_seeded):
    result = mdt.get_field_subset(
        ["head_word", "section", "orthographic_form", "frequency"], "messy_text"
    )
    # head_word/orthographic_form are on every doc; section is missing from one; frequency
    # is on none, so it drops out of the result entirely.
    assert len(result["head_word"]) == 5
    assert len(result["orthographic_form"]) == 5
    assert len(result["section"]) == 4
    assert "frequency" not in result
