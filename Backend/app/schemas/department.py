from datetime import datetime

from pydantic import BaseModel


class DepartmentResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
