import bcrypt
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from src.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:    
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def create_refresh_token(data: dict) -> str:
    expire = datetime.now() + timedelta(days=settings.refresh_expire_days)
    return jwt.encode({**data, "exp": expire}, settings.refresh_secret_key, algorithm=settings.algorithm)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now() + \
        (expires_delta if expires_delta else timedelta(
            minutes=settings.access_expire_token_min))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
