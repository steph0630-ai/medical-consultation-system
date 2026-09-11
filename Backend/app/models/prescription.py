from sqlalchemy import Boolean, Column, DECIMAL, ForeignKey, Integer, String

from app.models.base import BaseModel


class Prescription(BaseModel):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    appointment_id = Column(
        Integer, ForeignKey("appointments.id"), nullable=False, index=True
    )
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="pending", index=True)


class PrescriptionItem(BaseModel):
    __tablename__ = "prescription_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prescription_id = Column(
        Integer, ForeignKey("prescriptions.id"), nullable=False, index=True
    )
    drug_name = Column(String(200), nullable=False)
    dosage = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    drug_id = Column(Integer, ForeignKey("drugs.id"), nullable=True, index=True)
    unit_price = Column(DECIMAL(10, 2), nullable=True)
    is_selected = Column(Boolean, nullable=False, default=True, index=True)
