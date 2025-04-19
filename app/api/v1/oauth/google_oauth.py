import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import requests
from app.config import get_settings
from app.database import get_db
from app.models import User
from app.services.common_response import handle_success_response, handle_error_response

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
    try:
        auth_url = (
            f"{GOOGLE_AUTH_URL}"
            f"?response_type=code&client_id={GOOGLE_CLIENT_ID}"
            f"&redirect_uri={REDIRECT_URI}"
            f"&scope=openid%20email%20profile"
            f"&access_type=offline"
        )

        response = requests.get(auth_url)

        if response.status_code != 200:
            return handle_error_response(message="Error during Google OAuth login", error_details={"error": response.text},
                                         status_code=status.HTTP_400_BAD_REQUEST)

        return handle_success_response(message="Redirecting to Google OAuth", status_code=status.HTTP_302_FOUND,
                                       data={"url": auth_url})
    except Exception as e:
        return handle_error_response(message="Error during Google OAuth login", error_details={"error": str(e)},
                                     status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/auth/callback")
async def auth_callback(code: str = None, error: str = None, db: Session = Depends(get_db)):
    if error or not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authentication failed or code not provided"
        )
    try:
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

            userinfo_resp = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {tokens['access_token']}"}
            )
            userinfo_resp.raise_for_status()
            user_info = userinfo_resp.json()

            # Check if user exists
            existing_user = db.query(User).filter(User.email == user_info["email"]).first()
            if existing_user:
                # Update existing user
                existing_user.name = user_info["name"]
                db.commit()
                user = existing_user
            else:
                # Create new user
                new_user = User(
                    email=user_info["email"],
                    name=user_info["name"],
                    provider="google"
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                user = new_user

            return handle_success_response(
                message="Successfully authenticated",
                data={"email": user.email, "name": user.name},
                status_code=status.HTTP_200_OK
            )
    except httpx.HTTPError as e:
        return handle_error_response(
            message="Error during Google OAuth process",
            error_details={"error": str(e)},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return handle_error_response(
            message="Internal server error",
            error_details={"error": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )