from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
import firebase_admin
from firebase_admin import auth, credentials
import os, json
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
import requests
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer
from fastapi import Cookie
from models.user_models import UpdateProfileRequest
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

    # Exchange custom token for an ID token so we can set it as a session cookie
    sign_in_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={firebase_config['apiKey']}"
    sign_in_resp = requests.post(sign_in_url, json={"token": custom_token, "returnSecureToken": True})
    sign_in_data = sign_in_resp.json()
    id_token = sign_in_data.get("idToken")

    if not id_token:
        return JSONResponse({"error": "Failed to exchange custom token for session"}, status_code=400)

    response = RedirectResponse(url="/userspace", status_code=302)
    response.set_cookie(
        key="user_token",
        value=id_token,
        httponly=True,
        secure=os.getenv("ENV") == "PROD",
        samesite="Lax",
        max_age=36000
    )
    return response

@router.get("/signin")
def signin_handler(request: Request):
    context = {
        "request": request,
        "firebase_api_key": firebase_config.get("apiKey", ""),
        "firebase_project_id": firebase_config.get("project_id", ""),
        "firebase_app_id": os.getenv("FIREBASE_APP_ID", ""),
    }
    return templates.TemplateResponse("signin.html", context)

@router.get("/login")
async def login_handler():
    return RedirectResponse(url="/account/signin")

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

@router.post("/session-login")
async def session_login(request: Request):
    """Accept a Firebase ID token from client-side auth (e.g. Google popup) and set it as a session cookie."""
    data = await request.json()
    id_token = data.get("idToken")
    if not id_token:
        raise HTTPException(status_code=400, detail="ID token required")
    try:
        auth.verify_id_token(id_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    response = JSONResponse({"success": True})
    response.set_cookie(
        key="user_token",
        value=id_token,
        httponly=True,
        secure=os.getenv("ENV") == "PROD",
        samesite="Lax",
        max_age=36000
    )
    return response


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
