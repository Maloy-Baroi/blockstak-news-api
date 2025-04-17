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
    token_data: TokenData = Depends(verify_api_access),
    client: httpx.AsyncClient = Depends(get_newsapi_client),
    db: Session = Depends(get_db)
):
    """
    Fetch all news with pagination support
    """
    params = {
        "apiKey": settings.NEWSAPI_KEY,
        "page": page_no,
        "pageSize": page_size
    }
    
    try:
        response = await client.get("/top-headlines", params=params)
        response.raise_for_status()
        data = response.json()
        
        # Format response
        articles = data.get("articles", [])
        total = data.get("totalResults", 0)
        
        news_list = []
        for article in articles:
            news = {
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "url": article.get("url", ""),
                "published_at": article.get("publishedAt", datetime.utcnow().isoformat()),
                "source": article.get("source", {}).get("name", "Unknown"),
                "country": None
            }
            news_list.append(News(**news, id=0, created_at=datetime.utcnow()))
        
        return handle_success_response(
            data={
                "data": news_list,
                "total": total,
                "page_no": page_no,
                "page_size": page_size
            },
            message="News fetched successfully",
            status_code=status.HTTP_200_OK
        )
    
    except httpx.HTTPError as e:
        return handle_error_response(
            message="Failed to fetch news",
            status_code=status.HTTP_400_BAD_REQUEST, 
            error_details=str(e)
        )