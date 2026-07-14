"""Shared helpers for reading a user's saved vocabulary lists.

Factored out of the ``/userspace/list_details`` route so both that AJAX
endpoint and the dedicated list/study page can resolve a saved list to its
stored word pairs (handling the "shared with me" lookup and permissions)
and paginate the result the same way, without duplicating the logic.
"""


def resolve_list_words(storage, user_id, language, list_name, shared=False):
    """Resolve a saved list to its stored word pairs and access metadata.

    ``storage`` is the App-Storage database handle. Returns a tuple
    ``(words, permission, is_owner, owner_id)``:

      words       - list of ``[SIMPLE_LEMMA, SHORT_DEFINITION]`` pairs, an
                    empty list if the list exists but has no words, or
                    ``None`` if the list could not be found / access denied.
      permission  - the caller's permission on a shared list, else ``None``.
      is_owner    - ``True`` when the caller owns the list.
      owner_id    - the resolved owner's user id (needed for edits on shared
                    lists), or ``None`` when the list could not be resolved.
    """
    owner_id = user_id
    permission = None

    if shared:
        shared_doc = storage.lists.find_one(
            {"user_id": user_id}, {"shared_with_me": 1, "_id": 0}
        )
        if not shared_doc:
            return None, None, False, None

        for oid, langs in shared_doc.get("shared_with_me", {}).items():
            for shared_list in langs.get(language, []):
                name = (
                    shared_list["list_name"] if isinstance(shared_list, dict)
                    else shared_list
                )
                if name == list_name:
                    owner_id = oid
                    permission = (
                        shared_list.get("permission", "edit")
                        if isinstance(shared_list, dict) else "edit"
                    )
                    break
            if owner_id != user_id:
                break

        if not owner_id or owner_id == user_id:
            return None, None, False, None

    doc = storage.lists.find_one(
        {"user_id": owner_id, f"languages.{language}.name": list_name},
        {f"languages.{language}.$": 1, "_id": 0}
    )
    if not doc:
        return None, permission, owner_id == user_id, owner_id

    words = doc["languages"][language][0]["words"] or []
    return words, permission, owner_id == user_id, owner_id


def paginate_words(words, page, limit):
    """Slice ``words`` for ``page``/``limit`` and return the pagination meta.

    Returns ``(page_slice, pagination_meta)`` where ``pagination_meta`` matches
    the shape the front end already consumes.
    """
    total_words = len(words)
    total_pages = (total_words + limit - 1) // limit if total_words > 0 else 1
    start_idx = (page - 1) * limit
    page_slice = words[start_idx:start_idx + limit]

    pagination = {
        "current_page": page,
        "total_pages": total_pages,
        "total_words": total_words,
        "limit": limit,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }
    return page_slice, pagination
