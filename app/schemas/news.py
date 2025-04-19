from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import List, Optional
from datetime import datetime


class NewsBase(BaseModel):
    title: str
    description: str
    url: HttpUrl
    published_at: datetime
    source: str
    country: Optional[str] = None


class NewsCreate(NewsBase):
    pass


class NewsInDB(NewsBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class News(NewsInDB):
    pass


class NewsResponse(BaseModel):
    data: List[News]
    total: int
    page_no: int
    page_size: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    client_id: Optional[str] = None
