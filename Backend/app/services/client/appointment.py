from typing import List

from fastapi import status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.http_exceptions import APIException
from app.models.appointment import Appointment
from app.models.department import Department
from app.models.doctor import Doctor
from app.schemas.client.appointment import AppointmentCreate, AppointmentResponse


class AppointmentService:
    @staticmethod
    async def _to_response(
        db: AsyncSession, appointment: Appointment
    ) -> AppointmentResponse:
        doctor = (
            await db.execute(select(Doctor).where(Doctor.id == appointment.doctor_id))
        ).scalar_one_or_none()
        department = (
            await db.execute(
                select(Department).where(
                    Department.id == appointment.department_id
                )
            )
        ).scalar_one_or_none()
        response = AppointmentResponse.model_validate(appointment)
        if doctor:
            from app.models.admin import Admin

            admin = (
                await db.execute(select(Admin).where(Admin.id == doctor.admin_id))
            ).scalar_one_or_none()
            if admin:
                response.doctor_name = (
                    f"{admin.last_name}{admin.first_name}"
                    if admin.last_name and admin.first_name
                    else admin.email
                )
        if department:
            response.department_name = department.name
        return response

    @staticmethod
    async def create_appointment(
        db: AsyncSession,
        patient_id: int,
        appointment_data: AppointmentCreate,
    ) -> AppointmentResponse:
        doctor = (
            await db.execute(
                select(Doctor).where(Doctor.id == appointment_data.doctor_id)
            )
        ).scalar_one_or_none()
        if not doctor:
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Doctor not found",
            )
        department = (
            await db.execute(
                select(Department).where(
                    Department.id == appointment_data.department_id
                )
            )
        ).scalar_one_or_none()
        if not department:
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Department not found",
            )
        appointment = Appointment(
            patient_id=patient_id,
            doctor_id=appointment_data.doctor_id,
            department_id=appointment_data.department_id,
            appointment_time=appointment_data.appointment_time,
            status="pending",
        )
        db.add(appointment)
        await db.flush()
        await db.refresh(appointment)
        return await AppointmentService._to_response(db, appointment)

    @staticmethod
    async def get_my_appointments_query(db: AsyncSession, patient_id: int):
        return (
            select(Appointment)
            .where(Appointment.patient_id == patient_id)
            .order_by(Appointment.appointment_time.desc())
        )

    @staticmethod
    async def list_appointments(
        db: AsyncSession, appointments: List[Appointment]
    ) -> List[AppointmentResponse]:
        return [
            await AppointmentService._to_response(db, appointment)
            for appointment in appointments
        ]

    @staticmethod
    async def cancel_appointment(
        db: AsyncSession, patient_id: int, appointment_id: int
    ) -> bool:
        appointment = (
            await db.execute(
                select(Appointment).where(
                    Appointment.id == appointment_id,
                    Appointment.patient_id == patient_id,
                )
            )
        ).scalar_one_or_none()
        if not appointment:
            return False
        if appointment.status == "cancelled":
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Appointment already cancelled",
            )
        if appointment.status != "pending":
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Only a pending appointment can be cancelled",
            )
        await db.execute(
            update(Appointment)
            .where(Appointment.id == appointment_id)
            .values(status="cancelled")
        )
        return True


appointment_service = AppointmentService()
