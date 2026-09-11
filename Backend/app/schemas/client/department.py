from typing import Optional

from app.schemas.base import BaseResponseSchema, BaseSchema, add_padded_id


class DepartmentBase(BaseSchema):
    name: str
    description: Optional[str] = None


@add_padded_id()
class DepartmentResponse(BaseResponseSchema, DepartmentBase):
    padded_id: Optional[str] = None
