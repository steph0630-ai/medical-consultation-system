from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.exceptions.http_exceptions import APIException
from app.schemas.client.doctor import DoctorResponse
from app.schemas.response import ApiResponse
from app.services.client.doctor import doctor_service


router = APIRouter()


@router.get("", response_model=list[DoctorResponse])
async def list_doctors(
    department_id: int = None,
    db: AsyncSession = Depends(get_db),
):
    query = await doctor_service.get_doctors_query(
        db, department_id=department_id
    )
    doctors = (await db.execute(query)).scalars().all()
    response = await doctor_service.list_doctors(db, doctors)
    return ApiResponse.success(data=response)


@router.get("/{doctor_id}", response_model=DoctorResponse)
async def get_doctor(
    doctor_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await doctor_service.get_doctor(db, doctor_id)
    if not result:
        raise APIException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Doctor not found",
        )
    return ApiResponse.success(data=result)
