from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime

from app.database import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(Text)
    url = Column(String(512))
    published_at = Column(DateTime, default=datetime.utcnow)
    source = Column(String(100))
    country = Column(String(2))
    created_at = Column(DateTime, default=datetime.utcnow)