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
from models.user_models import AuthRequest, UpdateProfileRequest, PasswordChangeRequest
from mongo_connection import atlas_client
from datetime import datetime

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
        error_detail = str(e)
        if "EMAIL_EXISTS" in str(e):
            error_detail = "Email already exists"
        elif "INVALID_EMAIL" in str(e):
            error_detail = "Invalid email format"
        return JSONResponse(
                status_code=401, 
                content={"detail": error_detail}
            )

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
        try:
            error_data = res.json()
            message = (
                error_data.get("error", {})
                .get("message", "Invalid email or password")
                .replace("_", " ")
            )
        except ValueError:
            message = "Invalid email or password"

        return JSONResponse(
            status_code=401,  # force 401 for auth errors
            content={"detail": message}
        )

    data = res.json()
    id_token = data["idToken"]  
    refresh_token = data["refreshToken"]

    response = RedirectResponse(url="/userspace")
    response.set_cookie(
        key="user_token",
        value=id_token,
        httponly=True,
        secure=os.getenv("ENV") == "PROD", 
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
        raise HTTPException(status_code=401, detail="Not authorized")
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

@router.get("/profile")
async def get_profile(user=Depends(get_current_user_cookie)):
    """Get user profile information"""
    try:
        storage = atlas_client.get_database("App-Storage")

        # Get user profile from database
        user_doc = storage.user_profiles.find_one({"uid": user.get("uid")}, {"_id": 0})

        if not user_doc:
            # Create profile if it doesn't exist
            profile_data = {
                "uid": user.get("uid"),
                "email": user.get("email"),
                "display_name": user.get("name", ""),
                "created_at": datetime.now(),
                "last_login": datetime.now(),
                "is_active": True,
                "preferences": {
                    "language": "en",
                    "notifications_enabled": True,
                    "default_dictionary_language": "Latin",
                    "session_timeout_hours": 10
                }
            }
            storage.user_profiles.insert_one(profile_data)
            user_doc = profile_data
        else:
            # Update last login
            storage.user_profiles.update_one(
                {"uid": user.get("uid")},
                {"$set": {"last_login": datetime.now()}}
            )

        # Convert datetime objects to strings for JSON serialization
        if "created_at" in user_doc:
            user_doc["created_at"] = user_doc["created_at"].isoformat()
        if "last_login" in user_doc:
            user_doc["last_login"] = user_doc["last_login"].isoformat()

        return user_doc

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get profile: {str(e)}")

@router.put("/profile")
async def update_profile(
    payload: UpdateProfileRequest,
    user=Depends(get_current_user_cookie)
):
    """Update user profile"""
    try:
        storage = atlas_client.get_database("App-Storage")
        update_data = {}

        if payload.display_name is not None:
            update_data["display_name"] = payload.display_name
            # Also update in Firebase
            auth.update_user(user.get("uid"), display_name=payload.display_name)

        if payload.preferences is not None:
            update_data["preferences"] = payload.preferences.model_dump()

        if update_data:
            update_data["last_update"] = datetime.now()
            result = storage.user_profiles.update_one(
                {"uid": user.get("uid")},
                {"$set": update_data}
            )

            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="User profile not found")

        return {"success": True, "message": "Profile updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e)}")

@router.post("/change-password")
async def change_password(
    payload: PasswordChangeRequest,
    user=Depends(get_current_user_cookie)
):
    """Change user password"""
    try:
        # Verify current password by attempting to sign in
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_config['apiKey']}"
        body = {
            "email": user.get("email"),
            "password": payload.current_password,
            "returnSecureToken": True
        }

        res = requests.post(url, json=body)
        if res.status_code != 200:
            raise HTTPException(status_code=400, detail="Current password is incorrect")

        # Update password in Firebase
        auth.update_user(user.get("uid"), password=payload.new_password)

        # Log the password change
        storage = atlas_client.get_database("App-Storage")
        audit_entry = {
            "user_id": user.get("uid"),
            "action": "password_change",
            "resource": "user_account",
            "timestamp": datetime.now(),
            "success": True
        }
        storage.audit_logs.insert_one(audit_entry)

        return {"success": True, "message": "Password changed successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to change password: {str(e)}")

@router.get("/settings")
async def get_settings(request: Request, user=Depends(get_current_user_cookie)):
    """Get user settings page"""
    context = {"request": request}
    profile = await get_profile(user)
    context.update(profile)
    return templates.TemplateResponse("user_settings.html", context)

@router.delete("/account")
async def delete_account(user=Depends(get_current_user_cookie)):
    """Delete user account and all associated data"""
    try:
        user_id = user.get("uid")
        storage = atlas_client.get_database("App-Storage")

        # Delete user data
        storage.lists.delete_many({"user_id": user_id})
        storage.user_profiles.delete_one({"uid": user_id})

        # Remove user from shared lists
        storage.lists.update_many(
            {},
            {"$unset": {f"shared_with_me.{user_id}": ""}}
        )

        # Log the deletion before deleting Firebase account
        audit_entry = {
            "user_id": user_id,
            "action": "account_deletion",
            "resource": "user_account",
            "timestamp": datetime.now(),
            "success": True
        }
        storage.audit_logs.insert_one(audit_entry)

        # Delete Firebase account
        auth.delete_user(user_id)

        return {"success": True, "message": "Account deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete account: {str(e)}")
