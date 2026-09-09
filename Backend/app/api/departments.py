from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.department import Department
from app.schemas.department import DepartmentResponse

router = APIRouter()


@router.get("")
async def list_departments(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> dict:
    total = await db.scalar(select(func.count(Department.id))) or 0
    result = await db.execute(
        select(Department)
        .order_by(Department.name)
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    items = [
        DepartmentResponse.model_validate(item, from_attributes=True).model_dump(mode="json")
        for item in result.scalars()
    ]
    return {
        "code": 200,
        "message": "success",
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "per_page": per_page,
        },
    }
