from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
import firebase_admin
from firebase_admin import auth, credentials
import os, re, json
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
import requests
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer
from fastapi import Cookie


security = HTTPBearer()
router = APIRouter()
router_path = Path.cwd()
templates = Jinja2Templates(directory="templates")
load_dotenv()

if not firebase_admin._apps:
    firebase_config_str = os.getenv("FIREBASE_CONFIG")
    firebase_config = json.loads(firebase_config_str)
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)
    
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/firebase/google-callback")

@router.get("/google-login")
async def google_login():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"redirect_uri={GOOGLE_REDIRECT_URI}&"
        "response_type=code&"
        "scope=openid%20email%20profile&"
        "access_type=offline"
    )
    return RedirectResponse(google_auth_url)


@router.get("/google-callback")
async def google_callback(code: str):
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    token_resp = requests.post(token_url, data=token_data)
    token_json = token_resp.json()
    id_token = token_json.get("id_token")
    access_token = token_json.get("access_token")

    if not id_token:
        return JSONResponse(
            {"error": "Failed to get ID token from Google"}, status_code=400
        )

    userinfo_resp = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    userinfo = userinfo_resp.json()
    email = userinfo.get("email")
    name = userinfo.get("name")

    try:
        user = auth.get_user_by_email(email)
    except auth.UserNotFoundError:
        user = auth.create_user(email=email, display_name=name)

    custom_token = auth.create_custom_token(user.uid).decode("utf-8")

    redirect_url = f"/?firebase_token={custom_token}"
    return RedirectResponse(redirect_url)

@router.get("/signup")
def signup_handler(request: Request):
    context = {"request" : request}
    return templates.TemplateResponse("signup.html", context)

@router.get("/login")
def login_handler(request: Request):
    context = {"request" : request}
    return templates.TemplateResponse("login.html", context)

class AuthRequest(BaseModel):
    email: str
    password: str
    username: str = None

@router.post("/signup")
async def firebase_signup(payload: AuthRequest):
    try:
        email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not email_regex.match(payload.email):
            raise ValueError("Invalid email format")
        
        if len(payload.password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        auth.create_user(email=payload.email, password=payload.password, display_name=payload.username)
        login_result = await firebase_login(payload)
        
        return login_result
    except Exception as e:
        if "EMAIL_EXISTS" in str(e):
            raise HTTPException(status_code=401, detail="Email already exists")
        elif "INVALID_EMAIL" in str(e):
            raise HTTPException(status_code=401, detail="Invalid email format")
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/login")
async def firebase_login(payload: AuthRequest):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_config['apiKey']}"
    body = {
        "email": payload.email,
        "password": payload.password,
        "returnSecureToken": True
    }

    res = requests.post(url, json=body)
    if res.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    data = res.json()
    id_token = data["idToken"]  
    refresh_token = data["refreshToken"]

    response = RedirectResponse(url="/userspace")
    response.set_cookie(
        key="user_token",
        value=id_token,
        httponly=True,
        secure=True, 
        samesite="Lax",
        max_age=36000 # 10 hours
    )

    return response

@router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse("/")
    response.delete_cookie("user_token")
    return response

def get_current_user_cookie(user_token: str = Cookie(None)):
    if not user_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        decoded_token = auth.verify_id_token(user_token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")


@router.get("/protected")
async def protected_route(user=Depends(get_current_user_cookie)):
    return {"message": "You are authenticated!", "user": user}

@router.post("/forgot-password")
async def forgot_password(request: Request):
    data = await request.json()
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    try:
        reset_link = auth.generate_password_reset_link(email)
        # TODO: Send this link via email
        print(f"Password reset link for {email}: {reset_link}")
        return JSONResponse({"message": "Password reset link generated. Check your email."})
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
