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

@router.get("/notes")
def get_notes(request: Request):
    return {"notes": {
        "note1": "This is note 1.",
        "note2": "This is note 2.",
        "note3": "This is note 3."
    }}

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
        return {"vocab": {"Latin": [], "Greek": []}}

    vocab_summary = {}
    for language, lists in doc["languages"].items():
        vocab_summary[language] = [lst["name"] for lst in lists]
        
    return {"vocab": vocab_summary}


@router.get("/media")
def get_media(request: Request):
    return {"media": {
        "image1": "Image 1 URL or description.",
        "video1": "Video 1 URL or description.",
        "audio1": "Audio 1 URL or description."
    }}


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
        print(words)
    
    db_dicts = {"Latin": "bridge_latin_dictionary", "Greek": "bridge_greek_dictionary"}
    dict_name = db_dicts.get(language, "bridge_latin_dictionary")
    collection = dict_db.get_collection(dict_name)
    
    cursor = collection.find({"TITLE": {"$in": list(words)}})
    
    words_info_dict = {
    word_doc["TITLE"]: {k.replace("_", " "): v for k, v in word_doc.items() if k != "_id" and k != "TITLE" and v is not None}
        for word_doc in cursor
    }

    return JSONResponse(words_info_dict)
