from datetime import UTC, datetime, timedelta
from typing import Dict, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import AuthBase
from app.db.session import transaction
from app.exceptions.http_exceptions import APIException
from app.models.token import Token as UserToken
from app.models.user import User


class ClientAuthService(AuthBase):
    @staticmethod
    async def authenticate_user(
        db: AsyncSession, email: str, password: str
    ) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user or not user.verify_password(password):
            return None
        return user

    @staticmethod
    async def register(
        db: AsyncSession, email: str, password: str, first_name: str, last_name: str
    ) -> Dict:
        async with transaction(db):
            result = await db.execute(select(User).where(User.email == email))
            if result.scalar_one_or_none():
                raise APIException(status_code=400, message="Email already registered")
            user = User(
                email=email,
                hashed_password=User.get_password_hash(password),
                first_name=first_name,
                last_name=last_name,
                is_active=True,
                is_verified=True,
            )
            db.add(user)
            await db.flush()
            user_id = user.id
        return {"user_id": user_id, "email": email}

    @staticmethod
    async def login(db: AsyncSession, email: str, password: str) -> Dict:
        async with transaction(db):
            user = await ClientAuthService.authenticate_user(db, email, password)
            if not user:
                raise APIException(status_code=400, message="Incorrect email or password")
            if not user.is_active:
                raise APIException(status_code=400, message="User account is inactive")
            await db.execute(
                update(UserToken)
                .where(UserToken.user_id == user.id, UserToken.is_active == True)
                .values(is_active=False)
            )
            access_token = AuthBase.create_access_token(
                str(user.id),
                scope="client",
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            )
            refresh_token = AuthBase.create_refresh_token(str(user.id))
            db.add(
                UserToken(
                    user_id=user.id,
                    token=AuthBase.hash_token(refresh_token),
                    expires_at=datetime.now(UTC) + timedelta(days=7),
                    is_active=True,
                )
            )
            await db.flush()
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            }

    @staticmethod
    async def refresh_token(db: AsyncSession, refresh_token: str) -> Dict:
        payload = AuthBase.verify_token(refresh_token, scope="refresh")
        if not payload:
            raise APIException(status_code=401, message="Invalid refresh token")
        user_id = payload.get("sub")
        result = await db.execute(
            select(UserToken).where(
                UserToken.user_id == user_id, UserToken.is_active == True
            )
        )
        token = result.scalar_one_or_none()
        if not token or not AuthBase.verify_token_hash(refresh_token, token.token):
            raise APIException(
                status_code=401, message="Invalid or expired refresh token"
            )
        token.last_used_at = datetime.now(UTC)
        await db.commit()
        return {
            "access_token": AuthBase.create_access_token(
                user_id,
                scope="client",
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            ),
            "token_type": "bearer",
        }

    @staticmethod
    async def logout(db: AsyncSession, refresh_token: str) -> None:
        payload = AuthBase.verify_token(refresh_token, scope="client")
        if not payload:
            return
        result = await db.execute(
            select(UserToken).where(
                UserToken.user_id == payload.get("sub"), UserToken.is_active == True
            )
        )
        token = result.scalar_one_or_none()
        if token:
            token.is_active = False
            await db.commit()


client_auth_service = ClientAuthService()
