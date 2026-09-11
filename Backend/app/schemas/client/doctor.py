from typing import Optional

from app.schemas.base import BaseResponseSchema, add_padded_id


@add_padded_id()
class DoctorResponse(BaseResponseSchema):
    department_id: int
    title: Optional[str] = None
    introduction: Optional[str] = None
    padded_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    department_name: Optional[str] = None
