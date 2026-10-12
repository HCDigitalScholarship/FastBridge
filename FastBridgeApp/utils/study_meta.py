"""Ensure the ``study_meta`` collection exists with its indexes.

``study_meta`` holds per-user SM-2 review state, one document per
``(user_id, language, lemma, gloss)``. Progress is deliberately per word and
per language rather than per list: knowing ``amo`` counts everywhere it
appears, and a list is a filter over that one knowledge base. The
``[lemma, gloss]`` pair is the identity starring already uses, so homographs
keep separate schedules.

Known limitation: ``delete_words`` matches on lemma alone and knows nothing
about this collection, so removing a word from a list leaves its document
behind. Under per-word scoping that is mostly a feature - re-adding the word
restores your progress - and orphans only accumulate for words removed from
every list, which is not worth a cleanup job.
"""
from pymongo import ASCENDING
from pymongo.errors import OperationFailure
from mongo_connection import atlas_client

STUDY_META_KEY = [
    ("user_id", ASCENDING),
    ("language", ASCENDING),
    ("lemma", ASCENDING),
    ("gloss", ASCENDING),
]
STUDY_META_DUE = [
    ("user_id", ASCENDING),
    ("language", ASCENDING),
    ("due", ASCENDING),
]


def ensure_study_meta():
    """Idempotently create the collection and its indexes."""
    storage = atlas_client.get_database("App-Storage")
    if "study_meta" not in storage.list_collection_names():
        storage.create_collection("study_meta")
    # The old per-list index. Nothing was ever written under it, so dropping it
    # loses no state, and it is absent entirely on a fresh database.
    try:
        storage.study_meta.drop_index("user_lang_list_lemma")
    except OperationFailure:
        pass
    storage.study_meta.create_index(
        STUDY_META_KEY, unique=True, name="user_lang_lemma_gloss"
    )
    storage.study_meta.create_index(STUDY_META_DUE, name="user_lang_due")
