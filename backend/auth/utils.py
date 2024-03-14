from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Union, Any
from jose import jwt



ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "128840dbb03219a79bbe189423e47e79681e5741d5960a278ee9420654d5503d"
JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    return jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    return jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
