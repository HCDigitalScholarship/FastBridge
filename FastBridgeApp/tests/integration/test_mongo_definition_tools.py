"""Integration tests for the MongoDefinitionTools query functions.

These run against a real (local, temporary) MongoDB seeded by the `seeded` fixture in
conftest.py, so they exercise the actual database queries rather than mocked data. They
skip automatically when no local Mongo is reachable.
"""


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
