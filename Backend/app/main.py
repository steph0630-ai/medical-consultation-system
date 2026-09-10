from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import func, select

from app.api.appointments import router as appointment_router
from app.api.auth import router as auth_router
from app.api.departments import router as department_router
from app.api.doctors import router as doctor_router
from app.db import Base, SessionLocal, engine
from app import models  # noqa: F401
from app.models.department import Department
from app.models.doctor import Doctor

DEPARTMENTS = [
    ("心血管内科", "擅长高血压、冠心病、心律失常"),
    ("呼吸内科", "擅长诊治肺炎、哮喘、慢阻肺等呼吸系统疾病"),
    ("消化内科", "擅长诊治胃炎、胃溃疡、肝病等消化系统疾病"),
    ("神经内科", "擅长诊治脑卒中、癫痫、帕金森病、头痛等"),
    ("骨科", "擅长诊治骨折、关节炎、腰椎间盘突出等"),
    ("儿科", "擅长诊治儿童感冒、发热、腹泻及生长发育问题"),
]

DOCTORS = [
    ("心血管内科", "伟", "张", "主任医师", "擅长高血压、冠心病及心律失常诊治"),
    ("呼吸内科", "敏", "李", "副主任医师", "擅长肺炎、哮喘及慢性呼吸疾病诊治"),
    ("消化内科", "强", "王", "主任医师", "擅长胃肠道及肝胆疾病诊治"),
    ("神经内科", "芳", "赵", "副主任医师", "擅长头痛、癫痫及脑血管疾病诊治"),
    ("骨科", "磊", "陈", "主治医师", "擅长骨折、关节及脊柱疾病诊治"),
    ("儿科", "静", "刘", "主任医师", "擅长儿童常见病及生长发育问题诊治"),
]


@asynccontextmanager
async def lifespan(_: FastAPI):
    # ponytail: create_all is enough for the first schema; use Alembic before schema changes.
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    async with SessionLocal() as session:
        if not await session.scalar(select(func.count(Department.id))):
            session.add_all(
                Department(name=name, description=description)
                for name, description in DEPARTMENTS
            )
            await session.commit()
        if not await session.scalar(select(func.count(Doctor.id))):
            departments = {
                department.name: department.id
                for department in (await session.scalars(select(Department))).all()
            }
            session.add_all(
                Doctor(
                    department_id=departments[department_name],
                    first_name=first_name,
                    last_name=last_name,
                    title=title,
                    introduction=introduction,
                )
                for department_name, first_name, last_name, title, introduction in DOCTORS
            )
            await session.commit()
    yield
    await engine.dispose()


app = FastAPI(title="智能医疗咨询系统", lifespan=lifespan)
app.include_router(appointment_router, prefix="/api/v1/appointments", tags=["appointments"])
app.include_router(auth_router, prefix="/api/v1", tags=["client-auth"])
app.include_router(department_router, prefix="/api/v1/departments", tags=["departments"])
app.include_router(doctor_router, prefix="/api/v1/doctors", tags=["doctors"])


@app.get("/api/v1/config/health")
async def health() -> dict:
    return {
        "code": 200,
        "message": "success",
        "data": {"status": "healthy", "services": {"api": "up"}},
    }
