from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime


class NewsBase(BaseModel):
    title: str
    description: str
    url: str
    published_at: datetime
    source: str
    country: Optional[str] = None


class NewsCreate(NewsBase):
    pass


class NewsInDB(NewsBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class News(NewsInDB):
    pass


class NewsResponse(BaseModel):
    data: List[News]
    total: int
    page: int
    limit: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    client_id: Optional[str] = None