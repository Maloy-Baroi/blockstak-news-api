from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
# filepath: d:\Interview_Task\blockstak-news-api\app\auth.py
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from sqlalchemy.orm import Session

from app.config import get_settings
from app.schemas.news import TokenData

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt


def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        client_id: str = payload.get("sub")
        
        if client_id is None:
            raise credentials_exception
        
        token_data = TokenData(client_id=client_id)
        return token_data
    
    except jwt.PyJWTError:
        raise credentials_exception


def get_current_client(token: str = Depends(oauth2_scheme)):
    return verify_token(token)


def authenticate_client(client_id: str, client_secret: str):
    if client_id != settings.CLIENT_ID or client_secret != settings.CLIENT_SECRET:
        return False
    return True