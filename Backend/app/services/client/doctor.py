from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admin import Admin
from app.models.department import Department
from app.models.doctor import Doctor
from app.schemas.client.doctor import DoctorResponse


class DoctorService:
    @staticmethod
    async def _to_response(db: AsyncSession, doctor: Doctor) -> DoctorResponse:
        admin = (
            await db.execute(select(Admin).where(Admin.id == doctor.admin_id))
        ).scalar_one_or_none()
        department = (
            await db.execute(
                select(Department).where(Department.id == doctor.department_id)
            )
        ).scalar_one_or_none()
        response = DoctorResponse.model_validate(doctor)
        if admin:
            response.first_name = admin.first_name
            response.last_name = admin.last_name
        if department:
            response.department_name = department.name
        return response

    @staticmethod
    async def get_doctors_query(db: AsyncSession, department_id: int = None):
        query = select(Doctor)
        if department_id:
            query = query.where(Doctor.department_id == department_id)
        return query

    @staticmethod
    async def list_doctors(
        db: AsyncSession, doctors: List[Doctor]
    ) -> List[DoctorResponse]:
        return [await DoctorService._to_response(db, doctor) for doctor in doctors]

    @staticmethod
    async def get_doctor(
        db: AsyncSession, doctor_id: int
    ) -> Optional[DoctorResponse]:
        result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
        doctor = result.scalar_one_or_none()
        if not doctor:
            return None
        return await DoctorService._to_response(db, doctor)


doctor_service = DoctorService()
