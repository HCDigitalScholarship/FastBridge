from fastapi import APIRouter, Request, Depends, HTTPException, Cookie
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from .firebase_auth import get_current_user_cookie
from mongo_connection import dict_db, atlas_client
from datetime import datetime
import uuid
from utils.permissions import PermissionChecker
from models.user_models import (
    PermissionLevel, GrantPermissionRequest, ModifyPermissionRequest,
    RevokePermissionRequest, UnlinkListRequest, SaveSearchRequest
)
from firebase_admin import auth

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def userspace(request: Request, user=Depends(get_current_user_cookie)):
    if not request.cookies.get("user_token"):
        raise HTTPException(
                    status_code=401, detail="Not authorized"
                )
    context = {"request": request}
    context["username"] = user.get('name', 'Guest')  
    context["email"] = user.get('email', 'No email provided')
    context["user_id"] = user.get('uid', None)  
    return templates.TemplateResponse("userspace.html", context)


@router.get("/vocab")
def get_vocab(
    request: Request,
    page: int = 1,
    limit: int = 5,
    language_filter: str = None,
    user=Depends(get_current_user_cookie)
):
    user_id = user.get("uid", None)
    storage = atlas_client.get_database("App-Storage")

    if not user_id:
        return {"error": "No user logged in"}

    doc = storage.lists.find_one(
        {"user_id": user_id}, {"languages": 1, "shared_with_me": 1, "_id": 0}
    )

    # get user's vocabulary lists
    all_vocab_lists = []
    if doc and "languages" in doc:
        for language, lists in doc["languages"].items():
            if not lists: continue
            if language_filter and language != language_filter:
                continue
            for lst in lists:
                all_vocab_lists.append({
                    "name": lst["name"],
                    "language": language,
                    "word_count": len(lst.get("words", [])),
                    "type": "user"
                })

    # get shared vocabulary lists
    if doc and "shared_with_me" in doc:
        print("Here we are in the shared with me logic")
        for owner_id, langs in doc["shared_with_me"].items():
            owner_doc = storage.lists.find_one(
                {"user_id": owner_id}, {"languages": 1, "_id": 0}
            )
            if not owner_doc or "languages" not in owner_doc:
                continue

            for lang, list_details in langs.items():
                list_names = set()
                for curr_list in list_details:
                    list_names.add(curr_list.get("list_name"))
                if language_filter and lang != language_filter:
                    continue
                available = owner_doc["languages"].get(lang, [])
                for lst in available:
                    if lst.get("name") in list_names:
                        all_vocab_lists.append({
                            "name": lst["name"],
                            "language": lang,
                            "word_count": len(lst.get("words", [])),
                            "type": "shared"
                        })

    # Pagination logic
    total_lists = len(all_vocab_lists)
    total_pages = (total_lists + limit - 1) // limit if total_lists > 0 else 1
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_lists = all_vocab_lists[start_idx:end_idx]

    # Group paginated lists by language and type
    vocab_summary = {}
    shared_summary = {}

    for lst in paginated_lists:
        if lst["type"] == "user":
            vocab_summary.setdefault(lst["language"], []).append({
                "name": lst["name"],
                "word_count": lst["word_count"]
            })
        else:
            shared_summary.setdefault(lst["language"], []).append({
                "name": lst["name"],
                "word_count": lst["word_count"]
            })

    if not vocab_summary:
        vocab_summary = {"You haven't created any lists. <br> Create a new list in the 'Create List' tab": []}
    if not shared_summary:
        shared_summary = {"No Shared Lists": []}

    return {
        "vocab": vocab_summary,
        "shared_vocab": shared_summary,
        "pagination": {
            "current_page": page,
            "total_pages": total_pages,
            "total_lists": total_lists,
            "limit": limit,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }


@router.get("/words")
async def get_words(request: Request, language: str = "Latin", query: str = None):
    db_dicts = {"Latin": "bridge_latin_dictionary", "Greek": "bridge_greek_dictionary"}
    dict_name = db_dicts.get(language, "bridge_latin_dictionary")
    collection = dict_db.get_collection(dict_name)

    filter_query = {}
    if query:
        filter_query["SIMPLE_LEMMA"] = {"$regex": f"^{query}", "$options": "i"}

    cursor = collection.find(filter_query, {"SIMPLE_LEMMA": 1, "SHORT_DEFINITION": 1, "_id": 0}).limit(25)  
    words = [[doc["SIMPLE_LEMMA"], doc.get("SHORT_DEFINITION", "")]for doc in cursor if "SIMPLE_LEMMA" in doc]
    
    return {"words": words}

class ListCreate(BaseModel):
    list_name: str
    language: str
    words: list[list[str]]
    shared: bool = None

@router.post("/create_list")
async def create_list(payload: ListCreate, request: Request, user=Depends(get_current_user_cookie)):
    user_id = user.get('uid', None) 
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    storage = atlas_client.get_database("App-Storage")

    user_doc = storage.lists.find_one({"user_id": user_id})
    existing_names = []
    if user_doc:
        existing_names = [lst["name"] for lst in user_doc.get("languages", {}).get(payload.language, [])]

    base_name = payload.list_name
    new_name = base_name
    counter = 1
    while new_name in existing_names:
        new_name = f"{base_name} ({counter})"
        counter += 1

    new_list = {
        "name": new_name,
        "words": payload.words,
        "owner_id": user_id,
        "created_at": datetime.now().isoformat(),
        "share_links": {
            "copy": str(uuid.uuid4()),
            "linked": str(uuid.uuid4())
        }
    }

    # upsert = create doc if it doesn't exist yet
    storage.lists.update_one(
        {"user_id": user_id}, {"$push": {f"languages.{payload.language}": new_list}}, upsert=True
    )

    return {
        "success": True,
        "message": f"List '{new_name}' added to {payload.language} for user {user_id}.",
        "list": new_list
    }
    
@router.get("/list_details")
async def get_list_details(
    request: Request,
    language: str,
    list_name: str,
    page: int = 1,
    limit: int = 20,
    shared: bool = None,
    user=Depends(get_current_user_cookie)
):
    user_id = user.get('uid', None)
    storage = atlas_client.get_database("App-Storage")

    owner_id = user_id
    user_permission = None

    if shared:
        shared_doc = storage.lists.find_one({"user_id": user_id}, {"shared_with_me": 1, "_id": 0})
        if not shared_doc: return JSONResponse({})

        for oid, langs in shared_doc.get("shared_with_me", {}).items():
            shared_lists = langs.get(language, [])
            for shared_list in shared_lists:
                list_name_match = (
                    shared_list["list_name"] if isinstance(shared_list, dict)
                    else shared_list
                ) == list_name
                if list_name_match:
                    owner_id = oid
                    user_permission = (
                        shared_list.get("permission", "edit")
                        if isinstance(shared_list, dict)
                        else "edit"
                    )
                    break
            if owner_id != user_id:
                break

        if not owner_id or owner_id == user_id:
            return JSONResponse({})

        doc = storage.lists.find_one(
            {"user_id": owner_id, f"languages.{language}.name": list_name},
            {f"languages.{language}.$": 1, "_id": 0}
        )
    else:
        doc = storage.lists.find_one(
            {"user_id": user_id, f"languages.{language}.name": list_name},
            {f"languages.{language}.$": 1, "_id": 0}
        )

    if doc:
        words = doc["languages"][language][0]["words"]

    if not words:
        return JSONResponse({
            "words": {},
            "pagination": {
                "current_page": page,
                "total_pages": 0,
                "total_words": 0,
                "limit": limit,
                "has_next": False,
                "has_prev": False
            },
            "permission": user_permission,
            "is_owner": owner_id == user_id
        })

    # Pagination logic for words
    total_words = len(words)
    total_pages = (total_words + limit - 1) // limit if total_words > 0 else 1
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_words = words[start_idx:end_idx]

    db_dicts = {"Latin": "bridge_latin_dictionary", "Greek": "bridge_greek_dictionary"}
    dict_name = db_dicts.get(language, "bridge_latin_dictionary")
    collection = dict_db.get_collection(dict_name)

    columns = ["SIMPLE_LEMMA", "SHORT_DEFINITION", "LONG_DEFINITION",
            "PART_OF_SPEECH", "PRINCIPAL_PARTS", "TITLE"]

    projection = {col: 1 for col in columns}
    projection["_id"] = 0
    query_conditions = [{"$and": [{"SIMPLE_LEMMA": w[0]}, {"SHORT_DEFINITION": w[1]}]} for w in paginated_words]

    cursor = collection.find({"$or": query_conditions}, projection)

    words_info_dict = {
    word_doc["TITLE"]: {k.replace("_", " "): v for k, v in word_doc.items() if k != "_id" and k != "TITLE" and v is not None}
        for word_doc in cursor
    }

    return JSONResponse({
        "words": words_info_dict,
        "pagination": {
            "current_page": page,
            "total_pages": total_pages,
            "total_words": total_words,
            "limit": limit,
            "has_next": page < total_pages,
            "has_prev": page > 1
        },
        "permission": user_permission,
        "is_owner": owner_id == user_id
    })

@router.post("/update_list")
async def update_user_list(payload: ListCreate, user=Depends(get_current_user_cookie)):
    user_id = user.get("uid", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    storage = atlas_client.get_database("App-Storage")

    unique_words = [list(t) for t in {tuple(w) for w in payload.words}] # remove duplicates

    result = storage.lists.update_one(
        {
            "user_id": user_id,
            f"languages.{payload.language}.name": payload.list_name
        },
        {
            "$set": {
                f"languages.{payload.language}.$.words": unique_words,
                f"languages.{payload.language}.$.last_update": datetime.now().isoformat()
            }
        }
    )

    if result.matched_count == 0:
        return JSONResponse(
            {
                "success": False,
                "message": f"List '{payload.list_name}' in {payload.language} not found for user {user_id}."
            },
            status_code=404
        )

    return {
        "success": True,
        "message": f"List '{payload.list_name}' updated in {payload.language} for user {user_id}."
    }


@router.post("/delete_list")
async def delete_user_list(request: Request, user=Depends(get_current_user_cookie)):
    """
    Deletes the user's vocabulary list only if they are the owner.
    Also cleans up all permission grants and shared_with_me references.
    Expects JSON: { 'list_name': str, 'language': str }
    """
    user_id = user.get("uid")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    data = await request.json()
    list_name = data.get("list_name")
    language = data.get("language")

    if not list_name or not language:
        raise HTTPException(status_code=400, detail="Missing list_name or language")

    storage = atlas_client.get_database("App-Storage")

    # Get the list to find who has access
    doc = storage.lists.find_one(
        {"user_id": user_id, f"languages.{language}.name": list_name},
        {f"languages.{language}.$": 1}
    )

    if doc and "languages" in doc:
        target_list = doc["languages"][language][0]
        permissions = target_list.get("permissions", {})

        for recipient_id in permissions.keys():
            storage.lists.update_one(
                {"user_id": recipient_id},
                {
                    "$pull": {
                        f"shared_with_me.{user_id}.{language}": {
                            "list_name": list_name
                        }
                    }
                }
            )

    # Delete the list
    result = storage.lists.update_one(
        {"user_id": user_id},
        {"$pull": {f"languages.{language}": {"name": list_name, "owner_id": user_id}}}
    )

    if result.modified_count == 0:
        return JSONResponse(
            {
                "success": False,
                "message": f"List '{list_name}' in {language} not found or you are not the owner."
            },
            status_code=404
        )

    return {
        "success": True,
        "message": f"List '{list_name}' deleted from {user.get('username', '')} {language} List."
    }

@router.post("/add_shared_list")
async def add_shared_list(request: Request, user=Depends(get_current_user_cookie)):
    data = await request.json()
    share_link = data.get("share_link")
    language = data.get("language")
    mode = data.get("mode", "copy")  # default to copy

    if not share_link or not language:
        raise HTTPException(status_code=400, detail="Missing share_link or language")

    user_id = user.get("uid")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    storage = atlas_client.get_database("App-Storage")

    # Find the shared list by share_link
    doc = storage.lists.find_one(
        {f"languages.{language}.share_links.{mode}": share_link}
    )

    if not doc:
        raise HTTPException(status_code=404, detail="Shared list not found")

    owner_id = doc["user_id"]

    # Locate the exact list within the language
    shared_list = None
    for lst in doc.get("languages", {}).get(language, []):
        if lst.get("share_links", {}).get(mode) == share_link:
            shared_list = lst
            break

    if not shared_list:
        raise HTTPException(status_code=404, detail="Shared list not found in specified language")

    if mode == "copy":
        user_doc = storage.lists.find_one({"user_id": user_id})
        existing_names = []
        if user_doc:
            existing_names = [lst["name"] for lst in user_doc.get("languages", {}).get(language, [])]

        base_name = shared_list["name"]
        new_name = base_name
        counter = 1
        while new_name in existing_names:
            new_name = f"{base_name} (copy {counter})"
            counter += 1

        new_list = {
            "name": new_name,
            "words": shared_list["words"],
            "owner_id": user_id,
            "original_owner_id": shared_list.get("owner_id", owner_id),
            "created_at": datetime.now().isoformat(),
            "share_links": {
                "copy": str(uuid.uuid4()),
                "linked": str(uuid.uuid4())
            }
        }

        storage.lists.update_one(
            {"user_id": user_id},
            {"$push": {f"languages.{language}": new_list}},
            upsert=True
        )
        return {
            "success": True,
            "message": f"Copied list '{new_name}' added to {language}.",
        }

    elif mode == "linked":
        # Store pointer in `shared_with_me` with permissions
        permission = data.get("permission", "edit")  # Default permission for linked mode
        list_name = shared_list.get("name")
        if not list_name:
            raise HTTPException(status_code=500, detail="Shared list is missing a name")

        # Add permission to owner's list
        permission_grant = {
            "level": permission,
            "granted_at": datetime.now().isoformat(),
            "granted_by": owner_id  # Self-granted via share link
        }

        storage.lists.update_one(
            {
                "user_id": owner_id,
                f"languages.{language}.name": list_name
            },
            {
                "$set": {
                    f"languages.{language}.$.permissions.{user_id}": permission_grant
                }
            }
        )

        # Add to recipient's shared_with_me with permission
        shared_list_info = {
            "list_name": list_name,
            "permission": permission,
            "shared_at": datetime.now().isoformat()
        }

        storage.lists.update_one(
            {"user_id": user_id},
            {
                "$addToSet": {f"shared_with_me.{owner_id}.{language}": shared_list_info}
            },
            upsert=True
        )

        return {
            "success": True,
            "message": f"Linked list '{shared_list['name']}' added from {owner_id} under {language} with {permission} permission.",
        }

    else:
        raise HTTPException(status_code=400, detail="Invalid mode")


@router.get("/accept-list/{share_id}")
async def accept_list(share_id: str, user_token: str = Cookie(None)):
    if not user_token:
        return RedirectResponse(url=f"/account/signin?next=/userspace/accept-list/{share_id}", status_code=302)

    storage = atlas_client.get_database("App-Storage")
    session = storage.sessions.find_one(
        {"session_id": user_token, "expires_at": {"$gt": datetime.now()}},
        {"_id": 0}
    )
    if not session:
        return RedirectResponse(url="/account/signin", status_code=302)

    user_id = session["user_id"]

    # Find which list/language/mode this share_id belongs to
    languages = ["Latin", "Greek"]
    modes = ["copy", "linked"]
    owner_doc = language = list_name = mode = shared_list = None

    for lang in languages:
        for m in modes:
            doc = storage.lists.find_one({f"languages.{lang}.share_links.{m}": share_id})
            if doc:
                owner_doc = doc
                language = lang
                mode = m
                for lst in doc["languages"][lang]:
                    if lst.get("share_links", {}).get(m) == share_id:
                        shared_list = lst
                        list_name = lst["name"]
                        break
                break
        if owner_doc:
            break

    if not owner_doc or not shared_list:
        raise HTTPException(status_code=404, detail="Share link not found or expired")

    owner_id = owner_doc["user_id"]

    # Redirect to userspace if this is your own list
    if owner_id == user_id:
        return RedirectResponse(url="/userspace", status_code=302)

    if mode == "copy":
        # Create an independent copy
        user_doc = storage.lists.find_one({"user_id": user_id})
        existing_names = [lst["name"] for lst in (user_doc or {}).get("languages", {}).get(language, [])] if user_doc else []
        name = list_name
        counter = 1
        while name in existing_names:
            name = f"{list_name} (copy {counter})"
            counter += 1

        new_list = {
            "name": name,
            "words": shared_list["words"],
            "owner_id": user_id,
            "original_owner_id": shared_list.get("owner_id", owner_id),
            "created_at": datetime.now().isoformat(),
            "share_links": {"copy": str(uuid.uuid4()), "linked": str(uuid.uuid4())}
        }
        storage.lists.update_one(
            {"user_id": user_id},
            {"$push": {f"languages.{language}": new_list}},
            upsert=True
        )
    else:
        # Linked share — grant view permission by default
        permission_grant = {
            "level": "view",
            "granted_at": datetime.now().isoformat(),
            "granted_by": owner_id
        }
        storage.lists.update_one(
            {"user_id": owner_id, f"languages.{language}.name": list_name},
            {"$set": {f"languages.{language}.$.permissions.{user_id}": permission_grant}}
        )
        storage.lists.update_one(
            {"user_id": user_id},
            {"$addToSet": {f"shared_with_me.{owner_id}.{language}": {
                "list_name": list_name,
                "permission": "view",
                "shared_at": datetime.now().isoformat()
            }}},
            upsert=True
        )

    return RedirectResponse(url="/userspace", status_code=302)


@router.post("/add_words")
async def add_words(payload: ListCreate, user=Depends(get_current_user_cookie)):
    storage = atlas_client.get_database("App-Storage")
    user_id = user.get("uid")

    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    target_user_id = user_id

    if payload.shared:
        # Shared list - find owner and check permission
        doc = storage.lists.find_one(
            {"user_id": user_id}, {"shared_with_me": 1, "_id": 0}
        )
        owner_id = None
        if doc and "shared_with_me" in doc:
            for oid, langs in doc["shared_with_me"].items():
                shared_lists = langs.get(payload.language, [])
                for shared_list in shared_lists:
                    list_name_match = (
                        shared_list["list_name"] if isinstance(shared_list, dict)
                        else shared_list
                    ) == payload.list_name
                    if list_name_match:
                        owner_id = oid
                        break
                if owner_id:
                    break

        if not owner_id:
            raise HTTPException(status_code=404, detail="Shared list not found")

        # Check permission (requires at least EDIT permission)
        await PermissionChecker.require_permission(
            user_id, owner_id, payload.language, payload.list_name, PermissionLevel.EDIT
        )

        target_user_id = owner_id

    list_name = payload.list_name
    language = payload.language
    words_to_add = payload.words

    if not list_name or not language or not words_to_add:
        raise HTTPException(status_code=400, detail="Missing list_name, language, or words")

    # Append words to the existing list
    result = storage.lists.update_one(
        {"user_id": target_user_id, f"languages.{language}.name": list_name},
        {"$addToSet": {f"languages.{language}.$.words": {"$each": words_to_add}}}, upsert=False
    )

    if result.matched_count == 0:
        return JSONResponse(
            {"success": False, "message": f"List '{list_name}' in {language} not found."},
            status_code=404
        )

    return {
        "success": True,
        "message": f"Added {len(words_to_add)} words to list '{list_name}' in {language}.",
    }

class ShareListPayload(BaseModel):
    list_name: str
    language: str
    sharing_mode: str   # "copy" or "editable"

@router.post("/get_share_id", response_class=JSONResponse)
async def get_share_id(
    payload: ShareListPayload,
    request: Request,
    user=Depends(get_current_user_cookie)
):
    user_id = user.get('uid', None)
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    storage = atlas_client.get_database("App-Storage")

    # Directly query for the list inside the user's language sub-array
    doc = storage.lists.find_one(
        {"user_id": user_id, f"languages.{payload.language}.name": payload.list_name},
        {f"languages.{payload.language}.$": 1, "_id": 0}
    )

    if not doc:
        return {"success": False, "message": "List not found."}

    lst = doc["languages"][payload.language][0]
    share_links = lst.get("share_links", {})
    
    if payload.sharing_mode == "copy":
        share_id = share_links.get("copy")
    elif payload.sharing_mode == "editable":
        share_id = share_links.get("linked")
    else:
        return {"success": False, "message": "Invalid sharing mode."}

    if not share_id:
        return {"success": False, "message": "Share link not found."}

    base_url = str(request.base_url).rstrip("/")
    return {
        "success": True,
        "share_id": share_id,
        "share_url": f"{base_url}/userspace/accept-list/{share_id}"
    }


@router.post("/permissions/grant")
async def grant_permission(
    payload: GrantPermissionRequest,
    user=Depends(get_current_user_cookie)
):
    """
    Grant permission to another user for a linked list.
    Owner or admin users can grant permissions.
    """
    user_id = user.get("uid")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    storage = atlas_client.get_database("App-Storage")
    language = payload.language.value
    owner_id = payload.owner_id if payload.owner_id else user_id

    # avoid admin users from changing their permission
    if owner_id != user_id:
        await PermissionChecker.require_permission(
            user_id, owner_id, language, payload.list_name, PermissionLevel.ADMIN
        )

    # get list
    doc = storage.lists.find_one(
        {
            "user_id": owner_id,
            f"languages.{language}.name": payload.list_name
        },
        {f"languages.{language}.$": 1}
    )

    if not doc or "languages" not in doc or language not in doc["languages"]:
        raise HTTPException(status_code=404, detail="List not found")

    # Find recipient by email
    try:
        recipient = auth.get_user_by_email(payload.recipient_email)
        recipient_id = recipient.uid
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User with this email not found")

    # Cannot grant permission to owner (self-sharing check)
    if recipient_id == owner_id:
        raise HTTPException(status_code=400, detail="Cannot grant permissions to the list owner")

    # Add permission to owner's list
    permission_grant = {
        "level": payload.permission.value,
        "granted_at": datetime.now().isoformat(),
        "granted_by": user_id  # Track who granted it
    }

    result = storage.lists.update_one(
        {
            "user_id": owner_id,
            f"languages.{language}.name": payload.list_name
        },
        {
            "$set": {
                f"languages.{language}.$.permissions.{recipient_id}": permission_grant
            }
        }
    )

    # Add to recipient's shared_with_me
    shared_list_info = {
        "list_name": payload.list_name,
        "permission": payload.permission.value,
        "shared_at": datetime.now().isoformat()
    }

    storage.lists.update_one(
        {"user_id": recipient_id},
        {
            "$addToSet": {
                f"shared_with_me.{owner_id}.{language}": shared_list_info
            }
        },
        upsert=True
    )

    # Log the action
    audit_entry = {
        "user_id": user_id,
        "action": "grant_permission",
        "resource": f"list:{language}:{payload.list_name}",
        "timestamp": datetime.now(),
        "details": {
            "owner_id": owner_id,
            "recipient_id": recipient_id,
            "recipient_email": payload.recipient_email,
            "permission": payload.permission.value
        }
    }
    storage.audit_logs.insert_one(audit_entry)

    return {
        "success": True,
        "message": f"Granted {payload.permission.value} permission to {payload.recipient_email}"
    }

@router.post("/permissions/modify", response_class=JSONResponse)
async def modify_permission(
    payload: ModifyPermissionRequest,
    user=Depends(get_current_user_cookie)
):
    """
    Modify existing permission level for a user.
    Owner or admin users can modify permissions.
    """
    try:
        print(f"[MODIFY PERMISSION] Request from user {user.get('uid')} - Payload: {payload}")

        user_id = user.get("uid")
        if not user_id:
            return JSONResponse(
                status_code=401,
                content={"success": False, "detail": "User not authenticated"}
            )

        storage = atlas_client.get_database("App-Storage")

        # Extract the language value from enum
        language = payload.language.value

        owner_id = payload.owner_id if payload.owner_id else user_id

        print(f"[MODIFY PERMISSION] User: {user_id}, Owner: {owner_id}, Language: {language}, List: {payload.list_name}")

        # If modifying on someone else's list, check ADMIN permission
        if owner_id != user_id:
            await PermissionChecker.require_permission(
                user_id, owner_id, language, payload.list_name, PermissionLevel.ADMIN
            )

        # Verify list exists and permission exists
        doc = storage.lists.find_one(
            {
                "user_id": owner_id,
                f"languages.{language}.name": payload.list_name
            },
            {f"languages.{language}.$": 1}
        )

        if not doc:
            print(f"[MODIFY PERMISSION] List not found")
            return JSONResponse(
                status_code=404,
                content={"success": False, "detail": "List not found"}
            )

        if "languages" not in doc or language not in doc["languages"]:
            print(f"[MODIFY PERMISSION] Language not found in document")
            return JSONResponse(
                status_code=404,
                content={"success": False, "detail": "List not found"}
            )

        target_list = doc["languages"][language][0]
        permissions = target_list.get("permissions", {})

        if payload.recipient_id not in permissions:
            print(f"[MODIFY PERMISSION] Recipient does not have access to this list")
            return JSONResponse(
                status_code=404,
                content={"success": False, "detail": "User does not have access to this list"}
            )

        # Update permission in owner's list
        result = storage.lists.update_one(
            {
                "user_id": owner_id,
                f"languages.{language}.name": payload.list_name
            },
            {
                "$set": {
                    f"languages.{language}.$.permissions.{payload.recipient_id}.level": payload.new_permission.value,
                    f"languages.{language}.$.permissions.{payload.recipient_id}.granted_at": datetime.now().isoformat()
                }
            }
        )

        print(f"[MODIFY PERMISSION] Owner list update result: matched={result.matched_count}, modified={result.modified_count}")

        if result.modified_count == 0:
            return JSONResponse(
                status_code=500,
                content={"success": False, "detail": "Failed to update permission in owner's list"}
            )

        # Update in recipient's shared_with_me using filtered positional operator
        update_result = storage.lists.update_one(
            {
                "user_id": payload.recipient_id
            },
            {
                "$set": {
                    f"shared_with_me.{owner_id}.{language}.$[elem].permission": payload.new_permission.value
                }
            },
            array_filters=[{"elem.list_name": payload.list_name}]
        )

        print(f"[MODIFY PERMISSION] Recipient update result: matched={update_result.matched_count}, modified={update_result.modified_count}")

        # Check if recipient update succeeded
        if update_result.matched_count == 0:
            print(f"Warning: Could not find recipient document for user {payload.recipient_id}")
        elif update_result.modified_count == 0:
            print(f"Warning: Recipient's shared_with_me was not modified. List may not be in their shared_with_me.")

        # Log the action
        audit_entry = {
            "user_id": user_id,
            "action": "modify_permission",
            "resource": f"list:{language}:{payload.list_name}",
            "timestamp": datetime.now(),
            "details": {
                "recipient_id": payload.recipient_id,
                "new_permission": payload.new_permission.value
            }
        }
        storage.audit_logs.insert_one(audit_entry)

        print(f"[MODIFY PERMISSION] Success! Permission updated to {payload.new_permission.value}")

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": f"Permission updated to {payload.new_permission.value}"
            }
        )
    except Exception as e:
        print(f"[MODIFY PERMISSION] Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": f"Internal server error: {str(e)}"}
        )

@router.post("/permissions/revoke")
async def revoke_permission(
    payload: RevokePermissionRequest,
    user=Depends(get_current_user_cookie)
):
    """
    Revoke access from a user (owner action).
    Owner or admin users can revoke permissions.
    """
    user_id = user.get("uid")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    storage = atlas_client.get_database("App-Storage")

    language = payload.language.value

    owner_id = payload.owner_id if payload.owner_id else user_id

    # ensure user is an admin
    if owner_id != user_id:
        await PermissionChecker.require_permission(
            user_id, owner_id, language, payload.list_name, PermissionLevel.ADMIN
        )

    doc = storage.lists.find_one(
        {
            "user_id": owner_id,
            f"languages.{language}.name": payload.list_name
        },
        {f"languages.{language}.$": 1}
    )

    if not doc or "languages" not in doc or language not in doc["languages"]:
        raise HTTPException(status_code=404, detail="List not found")

    # Remove permission from owner's list
    result = storage.lists.update_one(
        {
            "user_id": owner_id,
            f"languages.{language}.name": payload.list_name
        },
        {
            "$unset": {
                f"languages.{language}.$.permissions.{payload.recipient_id}": ""
            }
        }
    )

    # Remove from recipient's shared_with_me
    storage.lists.update_one(
        {"user_id": payload.recipient_id},
        {
            "$pull": {
                f"shared_with_me.{owner_id}.{language}": {
                    "list_name": payload.list_name
                }
            }
        }
    )

    # Log
    audit_entry = {
        "user_id": user_id,
        "action": "revoke_permission",
        "resource": f"list:{language}:{payload.list_name}",
        "timestamp": datetime.now(),
        "details": {
            "recipient_id": payload.recipient_id
        }
    }
    storage.audit_logs.insert_one(audit_entry)

    return {
        "success": True,
        "message": "Access revoked successfully"
    }

@router.post("/permissions/unlink")
async def unlink_shared_list(payload: UnlinkListRequest, user=Depends(get_current_user_cookie)):
    """
    Remove shared list from user's shared_with_me (recipient action).
    Recipient can unlink lists shared with them.
    """
    user_id = user.get("uid")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    storage = atlas_client.get_database("App-Storage")

    language = payload.language.value
    doc = storage.lists.find_one(
        {"user_id": user_id},
        {f"shared_with_me.{payload.owner_id}.{language}": 1}
    )

    if not doc or "shared_with_me" not in doc:
        raise HTTPException(status_code=404, detail="Shared list not found")

    # Remove from recipient's shared_with_me
    result = storage.lists.update_one(
        {"user_id": user_id},
        {
            "$pull": {
                f"shared_with_me.{payload.owner_id}.{language}": {
                    "list_name": payload.list_name
                }
            }
        }
    )

    # Remove permission from owner's list
    storage.lists.update_one(
        {
            "user_id": payload.owner_id,
            f"languages.{language}.name": payload.list_name
        },
        {
            "$unset": {
                f"languages.{language}.$.permissions.{user_id}": ""
            }
        }
    )

    # Log
    audit_entry = {
        "user_id": user_id,
        "action": "unlink_list",
        "resource": f"list:{language}:{payload.list_name}",
        "timestamp": datetime.now(),
        "details": {
            "owner_id": payload.owner_id
        }
    }
    storage.audit_logs.insert_one(audit_entry)

    return {
        "success": True,
        "message": "List unlinked successfully"
    }

@router.post("/delete_words")
async def delete_words(request: Request, user=Depends(get_current_user_cookie)):
    """
    Delete specific words from a list (with permission support for shared lists).
    Requires ADMIN permission for shared lists, or ownership for own lists.
    """
    user_id = user.get("uid")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    data = await request.json()
    list_name = data.get("list_name")
    language = data.get("language")
    words_to_delete = data.get("words_to_delete", [])
    owner_id = data.get("owner_id", user_id)  # Default to current user if not specified

    if not list_name or not language or not words_to_delete:
        raise HTTPException(status_code=400, detail="Missing required parameters")

    storage = atlas_client.get_database("App-Storage")

    # If deleting from another user's list, check ADMIN permission
    if owner_id != user_id:
        await PermissionChecker.require_permission(
            user_id, owner_id, language, list_name, PermissionLevel.ADMIN
        )

    # Get list
    doc = storage.lists.find_one(
        {
            "user_id": owner_id,
            f"languages.{language}.name": list_name
        },
        {f"languages.{language}.$": 1}
    )

    if not doc or "languages" not in doc or language not in doc["languages"]:
        raise HTTPException(status_code=404, detail="List not found")

    target_list = doc["languages"][language][0]
    current_words = target_list.get("words", [])

    # Filter out words to delete (case-insensitive)
    words_to_delete_lower = [w.lower() for w in words_to_delete]
    filtered_words = [
        word for word in current_words
        if len(word) > 0 and word[0].lower() not in words_to_delete_lower
    ]

    # Update the list
    result = storage.lists.update_one(
        {
            "user_id": owner_id,
            f"languages.{language}.name": list_name
        },
        {
            "$set": {
                f"languages.{language}.$.words": filtered_words,
                f"languages.{language}.$.last_update": datetime.now().isoformat()
            }
        }
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to delete words")

    audit_entry = {
        "user_id": user_id,
        "action": "delete_words",
        "resource": f"list:{language}:{list_name}",
        "timestamp": datetime.now(),
        "details": {
            "owner_id": owner_id,
            "words_deleted": words_to_delete
        }
    }
    storage.audit_logs.insert_one(audit_entry)

    return {
        "success": True,
        "message": f"Deleted {len(words_to_delete)} word(s) from list"
    }

@router.get("/permissions/list")
async def get_list_permissions(
    language: str,
    list_name: str,
    owner_id: str = None,
    user=Depends(get_current_user_cookie)
):
    """
    Get all users who have access to a list.
    Owner or admin users can view permissions.
    """
    print("this should be here")
    user_id = user.get("uid")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    storage = atlas_client.get_database("App-Storage")

    # If owner_id not specified, assume current user is owner
    if not owner_id:
        owner_id = user_id

    # If requesting permissions for someone else's list, check ADMIN permission
    if owner_id != user_id:
        await PermissionChecker.require_permission(
            user_id, owner_id, language, list_name, PermissionLevel.ADMIN
        )

    # Find the list
    doc = storage.lists.find_one(
        {
            "user_id": owner_id,
            f"languages.{language}.name": list_name
        },
        {f"languages.{language}.$": 1, "_id": 0}
    )

    if not doc or "languages" not in doc or language not in doc["languages"]:
        raise HTTPException(status_code=404, detail="List not found")

    target_list = doc["languages"][language][0]
    permissions = target_list.get("permissions", {})

    permission_details = []
    for recipient_id, perm_data in permissions.items():
        try:
            recipient_user = auth.get_user(recipient_id)
            permission_details.append({
                "user_id": str(recipient_id),
                "email": recipient_user.email,
                "display_name": recipient_user.display_name or recipient_user.email,
                "permission": str(perm_data.get("level", "view")),
                "granted_at": str(perm_data.get("granted_at", "")),
                "granted_by": str(perm_data.get("granted_by", ""))
            })
        except Exception as e:
            print(f"Error getting user details for {recipient_id}: {e}")
            # User might have been deleted
            permission_details.append({
                "user_id": str(recipient_id),
                "email": "Unknown",
                "display_name": "Unknown User",
                "permission": str(perm_data.get("level", "view")),
                "granted_at": str(perm_data.get("granted_at", "")),
                "granted_by": str(perm_data.get("granted_by", ""))
            })

    return {
        "success": True,
        "list_name": str(list_name),
        "language": str(language),
        "permissions": permission_details
    }

@router.get("/permissions/shared-with-me")
async def get_shared_lists_summary(user=Depends(get_current_user_cookie)):
    """
    Get all lists shared with current user with their permissions.
    """
    user_id = user.get("uid")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    storage = atlas_client.get_database("App-Storage")

    doc = storage.lists.find_one(
        {"user_id": user_id},
        {"shared_with_me": 1, "_id": 0}
    )

    if not doc or "shared_with_me" not in doc:
        return {
            "success": True,
            "shared_lists": []
        }

    shared_lists = []
    for owner_id, langs in doc["shared_with_me"].items():
        try:
            owner_user = auth.get_user(owner_id)
            owner_name = owner_user.display_name or owner_user.email
        except Exception:
            owner_name = "Unknown User"

        for lang, lists in langs.items():
            for list_info in lists:
                if isinstance(list_info, dict):
                    shared_lists.append({
                        "owner_id": owner_id,
                        "owner_name": owner_name,
                        "language": lang,
                        "list_name": list_info["list_name"],
                        "permission": list_info["permission"],
                        "shared_at": list_info["shared_at"]
                    })
                else:
                    # Old format (backwards compatibility)
                    shared_lists.append({
                        "owner_id": owner_id,
                        "owner_name": owner_name,
                        "language": lang,
                        "list_name": list_info,
                        "permission": "edit",
                        "shared_at": None
                    })

    return {
        "success": True,
        "shared_lists": shared_lists
    }

@router.get("/permissions/my-shared-lists")
async def get_my_shared_lists(user=Depends(get_current_user_cookie)):
    """
    Get all lists owned by current user that are shared with others.
    """
    user_id = user.get("uid")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    storage = atlas_client.get_database("App-Storage")

    doc = storage.lists.find_one(
        {"user_id": user_id},
        {"languages": 1, "_id": 0}
    )

    if not doc or "languages" not in doc:
        return {
            "success": True,
            "my_shared_lists": []
        }

    my_shared_lists = []
    for lang, lists in doc["languages"].items():
        for lst in lists:
            if lst.get("owner_id") == user_id:
                permissions = lst.get("permissions", {})
                if permissions:
                    recipient_count = len(permissions)

                    permissions_list = []
                    for recipient_id, perm_data in permissions.items():
                        permissions_list.append({
                            "user_id": recipient_id,
                            "level": perm_data.get("level"),
                            "granted_at": perm_data.get("granted_at"),
                            "granted_by": perm_data.get("granted_by")
                        })

                    my_shared_lists.append({
                        "language": lang,
                        "list_name": lst["name"],
                        "word_count": len(lst.get("words", [])),
                        "recipient_count": recipient_count,
                        "permissions": permissions_list
                    })

    return {
        "success": True,
        "my_shared_lists": my_shared_lists
    }

# Saving Searches
@router.post("/save_search")
async def save_search(payload: SaveSearchRequest, user=Depends(get_current_user_cookie)):
    user_id = user.get("uid")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    storage = atlas_client.get_database("App-Storage")

    # Prevent duplicate names for same user
    existing = storage.saved_searches.find_one(
        {"user_id": user_id, "name": payload.name, "app": payload.app}
    )
    name = payload.name
    if existing:
        counter = 1
        while storage.saved_searches.find_one({"user_id": user_id, "name": f"{name} ({counter})", "app": payload.app}):
            counter += 1
        name = f"{name} ({counter})"

    doc = {
        "user_id": user_id,
        "search_id": str(uuid.uuid4()),
        "share_id": str(uuid.uuid4()),
        "app": payload.app,
        "name": name,
        "language": payload.language,
        "url": payload.url,
        "created_at": datetime.now().isoformat(),
    }
    storage.saved_searches.insert_one(doc)

    return {"success": True, "message": f"Search '{name}' saved.", "search_id": doc["search_id"]}


@router.get("/saved_searches")
async def get_saved_searches(
    user=Depends(get_current_user_cookie),
    app: str = None,
    language: str = None,
    name: str = None,
):
    user_id = user.get("uid")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    storage = atlas_client.get_database("App-Storage")
    query = {"user_id": user_id}
    if app:
        query["app"] = app
    if language:
        query["language"] = language
    if name:
        query["name"] = {"$regex": name, "$options": "i"}

    searches = list(storage.saved_searches.find(query, {"_id": 0}).sort("created_at", -1))
    return {"success": True, "searches": searches}


@router.post("/delete_search")
async def delete_search(request: Request, user=Depends(get_current_user_cookie)):
    user_id = user.get("uid")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    data = await request.json()
    search_id = data.get("search_id")
    if not search_id:
        raise HTTPException(status_code=400, detail="search_id required")

    storage = atlas_client.get_database("App-Storage")
    result = storage.saved_searches.delete_one({"user_id": user_id, "search_id": search_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Search not found")

    return {"success": True, "message": "Search deleted."}


@router.get("/get_search_share_link")
async def get_search_share_link(
    search_id: str,
    request: Request,
    user=Depends(get_current_user_cookie)
):
    user_id = user.get("uid")
    storage = atlas_client.get_database("App-Storage")
    search = storage.saved_searches.find_one(
        {"user_id": user_id, "search_id": search_id},
        {"share_id": 1, "_id": 0}
    )
    if not search:
        raise HTTPException(status_code=404, detail="Search not found")

    share_id = search.get("share_id")
    if not share_id:
        share_id = str(uuid.uuid4())
        storage.saved_searches.update_one(
            {"user_id": user_id, "search_id": search_id},
            {"$set": {"share_id": share_id}}
        )

    base_url = str(request.base_url).rstrip("/")
    return {"success": True, "share_url": f"{base_url}/userspace/accept-search/{share_id}"}


@router.get("/accept-search/{share_id}")
async def accept_search(share_id: str, user_token: str = Cookie(None)):
    if not user_token:
        return RedirectResponse(url=f"/account/signin?next=/userspace/accept-search/{share_id}", status_code=302)

    storage = atlas_client.get_database("App-Storage")
    session = storage.sessions.find_one(
        {"session_id": user_token, "expires_at": {"$gt": datetime.now()}},
        {"_id": 0}
    )
    if not session:
        return RedirectResponse(url="/account/signin", status_code=302)

    user_id = session["user_id"]

    source = storage.saved_searches.find_one({"share_id": share_id}, {"_id": 0})
    if not source:
        raise HTTPException(status_code=404, detail="Shared search not found")

    # If sharing with yourself just navigate to the search
    if source["user_id"] == user_id:
        return RedirectResponse(url=source["url"], status_code=302)

    # Name collision handling (same logic as save_search)
    name = source["name"]
    if storage.saved_searches.find_one({"user_id": user_id, "name": name, "app": source["app"]}):
        counter = 1
        while storage.saved_searches.find_one({"user_id": user_id, "name": f"{name} ({counter})", "app": source["app"]}):
            counter += 1
        name = f"{name} ({counter})"

    storage.saved_searches.insert_one({
        "user_id": user_id,
        "search_id": str(uuid.uuid4()),
        "share_id": str(uuid.uuid4()),
        "app": source["app"],
        "name": name,
        "language": source["language"],
        "url": source["url"],
        "created_at": datetime.now().isoformat(),
    })

    return RedirectResponse(url=source["url"], status_code=302)
