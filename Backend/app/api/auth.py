from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_token, decode_access_token, hash_password, verify_password
from app.db import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def success(data: object) -> dict:
    return {"code": 200, "message": "success", "data": data}


@router.post("/auth/register")
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)) -> dict:
    user = User(
        email=str(payload.email).lower(),
        hashed_password=hash_password(payload.password),
        first_name=payload.first_name,
        last_name=payload.last_name,
    )
    db.add(user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    await db.refresh(user)
    return success({"user_id": user.id, "email": user.email})


@router.post("/auth/login")
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(select(User).where(User.email == str(payload.email).lower()))
    user = result.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="User account is inactive")

    tokens = TokenResponse(
        access_token=create_token(
            user.id,
            "client",
            timedelta(minutes=settings.access_token_expire_minutes),
        ),
        refresh_token=create_token(user.id, "refresh", timedelta(days=7)),
    )
    return success(tokens.model_dump())


async def current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    user_id = decode_access_token(token)
    user = await db.get(User, user_id) if user_id is not None else None
    if not user or not user.is_active:
        raise HTTPException(status_code=403, detail="Invalid authentication credentials")
    return user


@router.get("/users/me")
async def me(user: User = Depends(current_user)) -> dict:
    return success(UserResponse.model_validate(user, from_attributes=True).model_dump(mode="json"))
