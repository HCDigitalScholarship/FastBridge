from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse
from .firebase_auth import get_current_user_cookie
from mongo_connection import dict_db, atlas_client
from datetime import datetime

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
        print(language, lists)
        if not lists: continue
        vocab_summary[language] = [lst["name"] for lst in lists]
    if not vocab_summary:
        vocab_summary = {"No Lists Found. <br> Create new list in the 'Create List' tab": []}
    return {"vocab": vocab_summary}


@router.get("/headwords")
async def get_headwords(request: Request, language: str = "Latin", query: str = None):
    db_dicts = {"Latin": "bridge_latin_dictionary", "Greek": "bridge_greek_dictionary"}
    dict_name = db_dicts.get(language, "bridge_latin_dictionary")
    collection = dict_db.get_collection(dict_name)

    filter_query = {}
    if query:
        filter_query["TITLE"] = {"$regex": f"^{query.upper()}"}

    cursor = collection.find(filter_query, {"TITLE": 1, "_id": 0}).limit(200)  
    headwords = [doc["TITLE"] for doc in cursor if "TITLE" in doc]
    
    return {"headwords": headwords}

class ListCreate(BaseModel):
    list_name: str
    language: str
    words: list[str]

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
        "created_at": datetime.now().isoformat(),
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
    
    db_dicts = {"Latin": "bridge_latin_dictionary", "Greek": "bridge_greek_dictionary"}
    dict_name = db_dicts.get(language, "bridge_latin_dictionary")
    collection = dict_db.get_collection(dict_name)
    
    cursor = collection.find({"TITLE": {"$in": list(words)}})
    
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

    # Try to replace the list with a matching name
    result = storage.lists.update_one(
        {
            "user_id": user_id,
            f"languages.{payload.language}.name": payload.list_name
        },
        {
            "$set": {
                f"languages.{payload.language}.$": {
                    "name": payload.list_name,
                    "words": payload.words,
                    "last_update": datetime.now().isoformat()
                }
            }
        }
    )

    if result.matched_count == 0:
        return JSONResponse(
            {"success": False, "message": f"List '{payload.list_name}' in {payload.language} not found for user {user_id}."},
            status_code=404
        )

    return {
        "success": True,
        "message": f"List '{payload.list_name}' updated in {payload.language} for user {user_id}.",
    }


@router.post("/delete_list")
async def delete_user_list(request: Request, user=Depends(get_current_user_cookie)):
    """
    Deletes the user's vocabulary list.
    Expects JSON: { 'list_name': str, 'language': str }
    """
    user_id = user.get("uid", None)
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
        {"$pull": {f"languages.{language}": {"name": list_name}}}
    )

    if result.modified_count == 0:
        return JSONResponse(
            {"success": False, "message": f"List '{list_name}' in {language} not found for user {user.get('username', '')}."},
            status_code=404
        )

    return {
        "success": True,
        "message": f"List '{list_name}' deleted from {user.get('username', '')} {language} List."
    }
