from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.exceptions.http_exceptions import APIException
from app.schemas.client.department import DepartmentResponse
from app.schemas.paginator import Paginator
from app.schemas.response import ApiResponse
from app.services.client.department import department_service


router = APIRouter()


@router.get("", response_model=list[DepartmentResponse])
async def list_departments(
    page: int = 1,
    per_page: int = 10,
    db: AsyncSession = Depends(get_db),
):
    query = await department_service.get_departments_query(db)
    result = await Paginator(query, db).paginate(page, per_page)
    result = result.map(DepartmentResponse)
    return result.response()


@router.get("/{department_id}", response_model=DepartmentResponse)
async def get_department(
    department_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await department_service.get_department(db, department_id)
    if not result:
        raise APIException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Department not found",
        )
    return ApiResponse.success(data=DepartmentResponse.model_validate(result))
