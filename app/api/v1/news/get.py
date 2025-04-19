from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
import httpx
from datetime import datetime

from app.api.dependencies import get_newsapi_client, verify_api_access
from app.config import get_settings
from app.database import get_db
from app.schemas.news import News, NewsResponse, TokenData
from app.services.common_response import handle_error_response, handle_success_response


settings = get_settings()
router = APIRouter()


@router.get("/news", response_model=NewsResponse)
async def get_news(
    page_no: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    client: httpx.AsyncClient = Depends(get_newsapi_client),
    db: Session = Depends(get_db)
):
    try:
        params = {
            "page": page_no,
            "pageSize": page_size,
            "country": "us"  # You can make this configurable if needed
        }
        resp = await client.get("/top-headlines", params=params)
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        # mirror the NewsAPI status code
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.text
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error fetching news"
        )

    data = resp.json()
    articles = data.get("articles", [])
    total = data.get("totalResults", 0)

    news_list = [
        News(
            id=0,
            title=a.get("title", ""),
            description=a.get("description", ""),
            url=a.get("url", ""),
            published_at=a.get("publishedAt", datetime.utcnow().isoformat()),
            source=a.get("source", {}).get("name", "Unknown"),
            country=None,
            created_at=datetime.utcnow()
        )
        for a in articles
    ]

    return NewsResponse(
        success=True,
        message="News fetched successfully",
        data=news_list,
        total=total,
        page_no=page_no,
        page_size=page_size
    )