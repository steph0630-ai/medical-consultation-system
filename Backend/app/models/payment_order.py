from sqlalchemy import Column, DECIMAL, ForeignKey, Index, Integer, String, TIMESTAMP, text

from app.models.base import BaseModel


class PaymentOrder(BaseModel):
    __tablename__ = "payment_orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=False, index=True)
    order_no = Column(String(40), nullable=False, unique=True, index=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    channel = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="pending", index=True)
    operator_type = Column(String(20), nullable=False)
    operator_id = Column(Integer, nullable=False)
    fail_reason = Column(String(200), nullable=True)
    paid_at = Column(TIMESTAMP(timezone=True), nullable=True)

    __table_args__ = (
        Index(
            "uq_payment_orders_bill_success",
            "bill_id",
            unique=True,
            postgresql_where=text("status = 'success'"),
        ),
    )
