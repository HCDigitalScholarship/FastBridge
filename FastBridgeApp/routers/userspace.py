from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse
from .firebase_auth import get_current_user_cookie
from mongo_connection import dict_db, atlas_client
from datetime import datetime
import uuid

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
def get_vocab(request: Request, user=Depends(get_current_user_cookie)):
    user_id = user.get("uid", None)
    storage = atlas_client.get_database("App-Storage")
    
    if not user_id:
        return {"error": "No user logged in"}

    doc = storage.lists.find_one(
        {"user_id": user_id}, {"languages": 1, "_id": 0}
    )

    if not doc or "languages" not in doc:
        return {"vocab": {"No lists Found. <br> Create new list in the 'Create List' tab": []}}

    vocab_summary = {}
    for language, lists in doc["languages"].items():
        if not lists: continue
        vocab_summary[language] = [lst["name"] for lst in lists]
    if not vocab_summary:
        vocab_summary = {"No Lists Found. <br> Create new list in the 'Create List' tab": []}
    return {"vocab": vocab_summary, "shared_vocab": vocab_summary}


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
async def get_list_details(request: Request, language: str, list_name: str, user=Depends(get_current_user_cookie)):
    user_id = user.get('uid', None)
    storage = atlas_client.get_database("App-Storage")

    doc = storage.lists.find_one(
        {"user_id": user_id, f"languages.{language}.name": list_name},
        {f"languages.{language}.$": 1, "_id": 0}  # the $ operator projects only the matched array element
    )

    if doc:
        words = doc["languages"][language][0]["words"]
    
    if not words:
        return JSONResponse({})
    
    db_dicts = {"Latin": "bridge_latin_dictionary", "Greek": "bridge_greek_dictionary"}
    dict_name = db_dicts.get(language, "bridge_latin_dictionary")
    collection = dict_db.get_collection(dict_name)

    columns = ["SIMPLE_LEMMA", "SHORT_DEFINITION", "LONG_DEFINITION", 
            "PART_OF_SPEECH", "PRINCIPAL_PARTS", "TITLE"]

    projection = {col: 1 for col in columns}
    projection["_id"] = 0
    query_conditions = [{"$and": [{"SIMPLE_LEMMA": w[0]}, {"SHORT_DEFINITION": w[1]}]} for w in words]
    
    cursor = collection.find({"$or": query_conditions}, projection)
    
    words_info_dict = {
    word_doc["TITLE"]: {k.replace("_", " "): v for k, v in word_doc.items() if k != "_id" and k != "TITLE" and v is not None}
        for word_doc in cursor
    }

    return JSONResponse(words_info_dict)

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
        # Just store a pointer in `shared_with_me`
        list_name = shared_list.get("name")
        if not list_name:
            raise HTTPException(status_code=500, detail="Shared list is missing an ID")

        storage.lists.update_one(
            {"user_id": user_id},
            {
                "$addToSet": {f"shared_with_me.{owner_id}.{language}": list_name}
            },
            upsert=True
        )

        return {
            "success": True,
            "message": f"Linked list '{shared_list['name']}' added from {owner_id} under {language}.",
        }

    else:
        raise HTTPException(status_code=400, detail="Invalid mode")

@router.post("/add_words")
async def add_words(payload: ListCreate, user=Depends(get_current_user_cookie)):
    user_id = user.get("uid")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    list_name = payload.list_name
    language = payload.language
    words_to_add = payload.words
    
    if not list_name or not language or not words_to_add:
        raise HTTPException(status_code=400, detail="Missing list_name, language, or words")

    storage = atlas_client.get_database("App-Storage")

    # Append words to the existing list
    result = storage.lists.update_one(
        {"user_id": user_id, f"languages.{language}.name": list_name},
        {"$addToSet": {f"languages.{language}.$.words": {"$each": words_to_add}}}, upsert=False
    )

    if result.matched_count == 0:
        return JSONResponse(
            {"success": False, "message": f"List '{list_name}' in {language} not found for user {user_id}."},
            status_code=404
        )

    return {
        "success": True,
        "message": f"Added {len(words_to_add)} words to list '{list_name}' in {language}.",
        "added_words": words_to_add
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
    
    return {"success": True, "share_id": share_id}
