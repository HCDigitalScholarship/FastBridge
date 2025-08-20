from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi import status as HTTP_403_FORBIDDEN
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .firebase_auth import get_current_user_cookie

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def userspace(request: Request, user=Depends(get_current_user_cookie)):
    if not request.cookies.get("user_token"):
        raise HTTPException(
                    status_code=404, detail="Not authorized"
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
def get_vocab(request: Request):
    return {"vocab": {
        "word1": "Definition for word 1.",
        "word2": "Definition for word 2.",
        "word3": "Definition for word 3."
    }}

@router.get("/media")
def get_media(request: Request):
    return {"media": {
        "image1": "Image 1 URL or description.",
        "video1": "Video 1 URL or description.",
        "audio1": "Audio 1 URL or description."
    }}