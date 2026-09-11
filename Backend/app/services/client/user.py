from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.client.user import UserProfileResponse


class UserService:
    @staticmethod
    async def get_profile(
        db: AsyncSession, user_id: int
    ) -> Optional[UserProfileResponse]:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        return UserProfileResponse.model_validate(user) if user else None

    @staticmethod
    async def update_profile(
        db: AsyncSession, user_id: int, profile_data: dict
    ) -> Optional[UserProfileResponse]:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return None
        allowed_fields = {"first_name", "last_name", "avatar", "gender"}
        update_data = {
            key: value for key, value in profile_data.items() if key in allowed_fields
        }
        if update_data:
            await db.execute(
                update(User).where(User.id == user_id).values(**update_data)
            )
            result = await db.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
        return UserProfileResponse.model_validate(user)


user_service = UserService()
