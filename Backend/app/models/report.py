from sqlalchemy import Column, ForeignKey, Integer, JSON, String, Text, TIMESTAMP

from app.models.base import BaseModel


class Report(BaseModel):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    appointment_id = Column(
        Integer, ForeignKey("appointments.id"), nullable=True, index=True
    )
    type = Column(String(50), nullable=False)
    content = Column(JSON, nullable=False)
    ai_interpretation = Column(Text, nullable=True)
    interpretation_status = Column(
        String(20), nullable=False, default="pending", index=True
    )
    interpretation_at = Column(TIMESTAMP(timezone=True), nullable=True)
    referenced_chunks = Column(JSON, nullable=True)
