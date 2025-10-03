from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from app.db import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(subject: int | str, expires_delta: timedelta | None = None, is_superuser: bool=False):
    to_encode = {"sub": str(subject)}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "is_superuser": is_superuser})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def decode_token(token: str):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    return payload
