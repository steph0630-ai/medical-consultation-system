from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import current_user
from app.db import get_db
from app.models.appointment import Appointment
from app.models.department import Department
from app.models.doctor import Doctor
from app.models.user import User
from app.schemas.appointment import AppointmentCreate

router = APIRouter()


def appointment_data(
    appointment: Appointment,
    doctor_name: str,
    department_name: str,
) -> dict:
    return {
        "id": appointment.id,
        "patient_id": appointment.patient_id,
        "doctor_id": appointment.doctor_id,
        "department_id": appointment.department_id,
        "doctor_name": doctor_name,
        "department_name": department_name,
        "appointment_time": appointment.appointment_time,
        "status": appointment.status,
        "created_at": appointment.created_at,
    }


@router.post("")
async def create_appointment(
    payload: AppointmentCreate,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    row = (
        await db.execute(
            select(Doctor, Department.name)
            .join(Department)
            .where(Doctor.id == payload.doctor_id)
        )
    ).one_or_none()
    if row is None:
        raise HTTPException(status_code=400, detail="Doctor not found")
    doctor, department_name = row
    if doctor.department_id != payload.department_id:
        raise HTTPException(status_code=400, detail="Doctor does not belong to department")

    appointment = Appointment(
        patient_id=user.id,
        doctor_id=doctor.id,
        department_id=doctor.department_id,
        appointment_time=payload.appointment_time,
    )
    db.add(appointment)
    await db.commit()
    await db.refresh(appointment)
    return {
        "code": 200,
        "message": "success",
        "data": appointment_data(
            appointment,
            f"{doctor.last_name}{doctor.first_name}",
            department_name,
        ),
    }


@router.get("")
async def list_appointments(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    total = await db.scalar(
        select(func.count(Appointment.id)).where(Appointment.patient_id == user.id)
    ) or 0
    rows = (
        await db.execute(
            select(Appointment, Doctor, Department.name)
            .join(Doctor, Doctor.id == Appointment.doctor_id)
            .join(Department, Department.id == Appointment.department_id)
            .where(Appointment.patient_id == user.id)
            .order_by(Appointment.appointment_time.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
        )
    ).all()
    return {
        "code": 200,
        "message": "success",
        "data": {
            "items": [
                appointment_data(
                    appointment,
                    f"{doctor.last_name}{doctor.first_name}",
                    department_name,
                )
                for appointment, doctor, department_name in rows
            ],
            "total": total,
            "page": page,
            "per_page": per_page,
        },
    }
