from fastapi import Depends
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from .schemas import TokenData
from sqlalchemy.orm import Session
from .functions.user import show


SECRET_KEY = "76b2baac6244d58ec777f733c1b64ac47bed23a91ef597a31d1ac1d07e0b8da1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        id: int = payload.get("id")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email, id=id)
    except jwt.JWTError:
        raise credentials_exception

    user = show(id, db)
    return user
