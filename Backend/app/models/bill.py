from sqlalchemy import Column, DECIMAL, ForeignKey, Integer, String, TIMESTAMP

from app.models.base import BaseModel


class Bill(BaseModel):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    appointment_id = Column(
        Integer, ForeignKey("appointments.id"), nullable=False, index=True
    )
    amount = Column(DECIMAL(10, 2), nullable=False)
    bill_type = Column(
        String(20), nullable=False, default="consultation", index=True
    )
    prescription_id = Column(
        Integer, ForeignKey("prescriptions.id"), nullable=True, index=True
    )
    status = Column(String(20), nullable=False, default="unpaid", index=True)
    paid_at = Column(TIMESTAMP(timezone=True), nullable=True)
    payment_method = Column(String(20), nullable=True)
    paid_by_type = Column(String(20), nullable=True)
    cashier_id = Column(Integer, ForeignKey("admins.id"), nullable=True, index=True)
