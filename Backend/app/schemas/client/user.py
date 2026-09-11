from typing import Optional

from pydantic import EmailStr

from app.schemas.base import BaseResponseSchema, BaseSchema, add_padded_id


@add_padded_id()
class UserProfileResponse(BaseResponseSchema):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    is_active: bool
    is_verified: bool
    padded_id: Optional[str] = None


class UserProfileUpdate(BaseSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
