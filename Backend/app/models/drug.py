from sqlalchemy import Boolean, Column, DECIMAL, Integer, String

from app.models.base import BaseModel


class Drug(BaseModel):
    __tablename__ = "drugs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), unique=True, nullable=False, index=True)
    spec = Column(String(100), nullable=True)
    unit = Column(String(20), nullable=False, default="盒")
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
