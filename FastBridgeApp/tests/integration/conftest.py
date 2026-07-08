"""Integration-test harness: a throwaway local MongoDB.

The Phase 3b tests run the real MongoDefinitionTools query functions against a local Mongo
seeded with a tiny fixture corpus. We point the connection at localhost using the Phase 0
env vars, seed two collections, and drop them afterwards. Nothing connects to Atlas and no
production data is touched. If a local Mongo isn't reachable, these tests skip instead of
failing.
"""
import os
import socket
import sys

import pytest

LOCAL_MONGO_URI = "mongodb://localhost:27017"


def _mongo_port_open(host="localhost", port=27017, timeout=0.5):
    """Quick check so the tests skip instantly when no Mongo is running, instead of
    waiting out the driver's 30-second connection timeout."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False

# Point the connection at the local Mongo before MongoDefinitionTools is imported.
os.environ["MONGO_URI"] = LOCAL_MONGO_URI
os.environ["MONGO_TLS"] = "false"
os.environ["MONGO_DB_NAME"] = "Latin-Texts"
os.environ["MONGO_DICT_DB_NAME"] = "dictionaries"


@pytest.fixture(scope="session")
def mdt():
    if not _mongo_port_open():
        pytest.skip("local MongoDB not reachable on localhost:27017")
    # Force a fresh import so the connection binds to the local Mongo, not any version a
    # previous test may have mocked into sys.modules.
    for name in ("MongoDefinitionTools", "mongo_connection"):
        sys.modules.pop(name, None)
    try:
        import MongoDefinitionTools as module
        module.atlas_client.ping()
    except Exception as exc:  # Mongo down, wrong port, etc.
        pytest.skip(f"local MongoDB not available ({exc})")
    return module


@pytest.fixture
def seeded(mdt):
    client = mdt.atlas_client.mongodb_client
    latin = client["Latin-Texts"]
    dictionaries = client["dictionaries"]

    latin.drop_collection("fixture_text")
    latin["fixture_text"].insert_many([
        {"counter": 1, "head_word": "AMO",    "orthographic_form": "amo",    "location": "1_1", "section": "1"},
        {"counter": 2, "head_word": "AMAS",   "orthographic_form": "amas",   "location": "1_1", "section": "1"},
        {"counter": 3, "head_word": "PUELLA", "orthographic_form": "puella", "location": "1_2", "section": "1"},
        {"counter": 4, "head_word": "REX",    "orthographic_form": "rex",    "location": "1_2", "section": "1"},
    ])

    dictionaries.drop_collection("fixture_dict")
    dictionaries["fixture_dict"].insert_many([
        {"TITLE": "amo",    "SIMPLE_LEMMA": "amo",    "SHORT_DEFINITION": "to love"},
        {"TITLE": "puella", "SIMPLE_LEMMA": "puella", "SHORT_DEFINITION": "girl"},
    ])

    # The query functions map a display title to a collection name via this production dict.
    # Add a temporary in-memory entry for the fixture and remove it afterwards.
    mdt.title_renaming_dict["Fixture Text"] = "fixture_text"

    yield

    latin.drop_collection("fixture_text")
    dictionaries.drop_collection("fixture_dict")
    mdt.title_renaming_dict.pop("Fixture Text", None)


@pytest.fixture
def messy_seeded(mdt):
    """A deliberately messy corpus, unlike the clean 4-row `seeded` fixture.

    Real texts carry the mess that actually breaks the corpus-load path: a document with no
    `section`, a null `location`, a gap in `counter`, an out-of-order `counter`, and repeated
    consecutive locations. Also registers an "Empty Text" that maps to a collection which is
    never created, for the empty-corpus case.
    """
    client = mdt.atlas_client.mongodb_client
    latin = client["Latin-Texts"]

    latin.drop_collection("messy_text")
    latin["messy_text"].insert_many([
        {"counter": 1, "head_word": "ALPHA",   "orthographic_form": "alpha",   "location": "1_1", "section": "1"},
        {"counter": 2, "head_word": "BETA",    "orthographic_form": "beta",    "location": "1_1"},               # no section
        {"counter": 3, "head_word": "EPSILON", "orthographic_form": "epsilon", "location": None, "section": "1"},# null location
        {"counter": 5, "head_word": "DELTA",   "orthographic_form": "delta",   "location": "1_2", "section": "1"},# counter gap (4 missing)
        {"counter": 4, "head_word": "GAMMA",   "orthographic_form": "gamma",   "location": "1_2", "section": "1"},# out-of-order counter, dup location
    ])
    mdt.title_renaming_dict["Messy Text"] = "messy_text"
    mdt.title_renaming_dict["Empty Text"] = "empty_text"

    yield

    latin.drop_collection("messy_text")
    mdt.title_renaming_dict.pop("Messy Text", None)
    mdt.title_renaming_dict.pop("Empty Text", None)


@pytest.fixture
def filter_texts(mdt):
    """Two overlapping texts so the include/exclude filters (the intended word-removal
    feature) can be asserted: 'include' keeps A ∩ B, 'exclude' keeps A - B.

    A = {AMO, AMAS, PUELLA, REX}; B = {PUELLA, REX, LUNA}. PUELLA/REX are the shared words.
    """
    client = mdt.atlas_client.mongodb_client
    latin = client["Latin-Texts"]

    latin.drop_collection("filter_text_a")
    latin["filter_text_a"].insert_many([
        {"counter": 1, "head_word": "AMO",    "orthographic_form": "amo",    "location": "1_1", "section": "1"},
        {"counter": 2, "head_word": "AMAS",   "orthographic_form": "amas",   "location": "1_1", "section": "1"},
        {"counter": 3, "head_word": "PUELLA", "orthographic_form": "puella", "location": "1_2", "section": "1"},
        {"counter": 4, "head_word": "REX",    "orthographic_form": "rex",    "location": "1_2", "section": "1"},
    ])
    latin.drop_collection("filter_text_b")
    latin["filter_text_b"].insert_many([
        {"counter": 1, "head_word": "PUELLA", "orthographic_form": "puella", "location": "1_1", "section": "1"},
        {"counter": 2, "head_word": "REX",    "orthographic_form": "rex",    "location": "1_1", "section": "1"},
        {"counter": 3, "head_word": "LUNA",   "orthographic_form": "luna",   "location": "1_2", "section": "1"},
    ])
    mdt.title_renaming_dict["Filter Text A"] = "filter_text_a"
    mdt.title_renaming_dict["Filter Text B"] = "filter_text_b"

    yield

    latin.drop_collection("filter_text_a")
    latin.drop_collection("filter_text_b")
    mdt.title_renaming_dict.pop("Filter Text A", None)
    mdt.title_renaming_dict.pop("Filter Text B", None)


@pytest.fixture
def leading_null_seeded(mdt):
    """A corpus whose first document (by counter) has a null location.

    This is the ordering `messy_seeded` deliberately avoids: mg_get_locations references its
    local `key` before assigning it, so the get_index path raises on the very first document.
    Kept separate so it can drive an xfail regression around that prod bug.
    """
    client = mdt.atlas_client.mongodb_client
    latin = client["Latin-Texts"]

    latin.drop_collection("leading_null_text")
    latin["leading_null_text"].insert_many([
        {"counter": 1, "head_word": "ALPHA", "orthographic_form": "alpha", "location": None,  "section": "1"},
        {"counter": 2, "head_word": "BETA",  "orthographic_form": "beta",  "location": "1_1", "section": "1"},
    ])
    mdt.title_renaming_dict["Leading Null Text"] = "leading_null_text"

    yield

    latin.drop_collection("leading_null_text")
    mdt.title_renaming_dict.pop("Leading Null Text", None)
