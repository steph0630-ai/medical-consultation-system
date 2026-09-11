from datetime import datetime
from typing import Optional

from app.schemas.base import BaseResponseSchema, BaseSchema, add_padded_id


class AppointmentCreate(BaseSchema):
    doctor_id: int
    department_id: int
    appointment_time: datetime


@add_padded_id()
class AppointmentResponse(BaseResponseSchema):
    patient_id: int
    doctor_id: int
    department_id: int
    appointment_time: datetime
    status: str
    padded_id: Optional[str] = None
    doctor_name: Optional[str] = None
    department_name: Optional[str] = None
