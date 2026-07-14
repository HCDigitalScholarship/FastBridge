"""Ensure the ``study_meta`` collection exists with its unique key index.

``study_meta`` backs per-user, per-word study state (starring lands here in
Phase 3). Fields are intentionally left open for now; the collection is keyed
by ``(user_id, language, list_name, lemma)`` so each word in a user's list has
at most one study-meta document.
"""
from pymongo import ASCENDING
from mongo_connection import atlas_client

STUDY_META_KEY = [
    ("user_id", ASCENDING),
    ("language", ASCENDING),
    ("list_name", ASCENDING),
    ("lemma", ASCENDING),
]


def ensure_study_meta():
    """Idempotently create the collection and its unique compound index."""
    storage = atlas_client.get_database("App-Storage")
    if "study_meta" not in storage.list_collection_names():
        storage.create_collection("study_meta")
    storage.study_meta.create_index(
        STUDY_META_KEY, unique=True, name="user_lang_list_lemma"
    )
