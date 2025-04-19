import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import RedirectResponse
import requests
import json

from urllib3 import request

from app.config import get_settings
from app.services.common_response import handle_success_response

settings = get_settings()

router = APIRouter()

# Configuration - update the redirect URI to match what's in your credentials
GOOGLE_CLIENT_ID = settings.CLIENT_ID
GOOGLE_CLIENT_SECRET = settings.CLIENT_SECRET
REDIRECT_URI = "http://localhost:8000/api/v1/auth/callback"  # Updated to match your credentials
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


# Redirect to Google's OAuth page
@router.get("/login/google")
async def login_google():
    auth_url = (
        f"{GOOGLE_AUTH_URL}"
        f"?response_type=code&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=openid%20email%20profile"
        f"&access_type=offline"
    )

    response = requests.get(auth_url)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to redirect to Google OAuth")

    return handle_success_response(message="Redirecting to Google OAuth", status_code=status.HTTP_302_FOUND, data={"url": auth_url})


@router.get("/auth/callback")
async def auth_callback(code: str = None, error: str = None):
    if error or not code:
        raise HTTPException(...)
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            GOOGLE_TOKEN_URL,
            data={
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": REDIRECT_URI,
            },
        )
        token_resp.raise_for_status()
        tokens = token_resp.json()
        # now fetch userinfo
        userinfo_resp = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {tokens['access_token']}"}
        )
        userinfo_resp.raise_for_status()
        user = userinfo_resp.json()
    # create or fetch a local user record, issue your own JWT, etc.

    return {"email": user["email"], "name": user["name"]}
