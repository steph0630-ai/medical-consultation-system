from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_context.verify(password, password_hash)


def create_token(subject: int, scope: str, expires: timedelta) -> str:
    payload = {
        "sub": str(subject),
        "scope": scope,
        "exp": datetime.now(timezone.utc) + expires,
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def decode_access_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        if payload.get("scope") != "client":
            return None
        return int(payload["sub"])
    except (JWTError, KeyError, TypeError, ValueError):
        return None
