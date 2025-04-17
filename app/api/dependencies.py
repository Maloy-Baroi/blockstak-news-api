import httpx
from fastapi import Depends, HTTPException, status
from typing import Dict, Any

from app.config import get_settings
from app.auth import get_current_client
from app.schemas import TokenData

settings = get_settings()

async def get_newsapi_client():
    async with httpx.AsyncClient(base_url=settings.NEWSAPI_BASE_URL) as client:
        yield client


def verify_api_access(token_data: TokenData = Depends(get_current_client)):
    if not token_data.client_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data