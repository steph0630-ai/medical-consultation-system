from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.department import Department
from app.models.doctor import Doctor

router = APIRouter()


def doctor_data(doctor: Doctor, department_name: str) -> dict:
    return {
        "id": doctor.id,
        "department_id": doctor.department_id,
        "department_name": department_name,
        "first_name": doctor.first_name,
        "last_name": doctor.last_name,
        "title": doctor.title,
        "introduction": doctor.introduction,
        "created_at": doctor.created_at,
    }


@router.get("")
async def list_doctors(
    department_id: int | None = Query(None, ge=1),
    db: AsyncSession = Depends(get_db),
) -> dict:
    query = select(Doctor, Department.name).join(Department)
    if department_id is not None:
        query = query.where(Doctor.department_id == department_id)
    rows = (await db.execute(query.order_by(Doctor.id))).all()
    return {
        "code": 200,
        "message": "success",
        "data": [doctor_data(doctor, department_name) for doctor, department_name in rows],
    }


@router.get("/{doctor_id}")
async def get_doctor(doctor_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    row = (
        await db.execute(
            select(Doctor, Department.name)
            .join(Department)
            .where(Doctor.id == doctor_id)
        )
    ).one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    doctor, department_name = row
    return {"code": 200, "message": "success", "data": doctor_data(doctor, department_name)}
