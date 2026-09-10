from datetime import datetime, timezone

from pydantic import BaseModel, field_validator


class AppointmentCreate(BaseModel):
    doctor_id: int
    department_id: int
    appointment_time: datetime

    @field_validator("appointment_time")
    @classmethod
    def future_time(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("appointment_time must include a timezone")
        if value <= datetime.now(timezone.utc):
            raise ValueError("appointment_time must be in the future")
        return value
