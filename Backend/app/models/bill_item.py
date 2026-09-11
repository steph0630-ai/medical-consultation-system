from sqlalchemy import Column, DECIMAL, ForeignKey, Integer, String

from app.models.base import BaseModel


class BillItem(BaseModel):
    __tablename__ = "bill_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=False, index=True)
    item_type = Column(String(20), nullable=False)
    name = Column(String(200), nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    subtotal = Column(DECIMAL(10, 2), nullable=False)
