from fastapi import APIRouter, HTTPException
from typing import List

# Create router instance
router = APIRouter(
    prefix="/news",
    tags=["news"],
    responses={404: {"description": "Not found"}},
)

# @router.get("/")
# async def get_news():
#     """
#     Get all news articles
#     """
#     try:
#         return {"message": "Get news endpoint"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))