import re

from pydantic import EmailStr, Field, field_validator

from app.schemas.base import BaseSchema


class Login(BaseSchema):
    email: EmailStr
    password: str


class Register(BaseSchema):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.search(r"[A-Za-z]", value):
            raise ValueError("密码必须包含至少一个字母")
        if not re.search(r"\d", value):
            raise ValueError("密码必须包含至少一个数字")
        return value


class Token(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshToken(BaseSchema):
    refresh_token: str


class Logout(BaseSchema):
    refresh_token: str
