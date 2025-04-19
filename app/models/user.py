from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from datetime import datetime

from app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), index=True)
    name = Column(Text)
    provider = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)