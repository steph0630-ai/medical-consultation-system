"""Complete database initial baseline.

Revision ID: 7d2a61f4c9be
Revises:
Create Date: 2026-09-02
"""
from typing import Optional, Sequence, Union

from alembic import op


revision: str = "7d2a61f4c9be"
down_revision: Optional[str] = None
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None

BASELINE_TABLES = {
    "admins",
    "admin_tokens",
    "appointments",
    "bills",
    "bill_items",
    "departments",
    "dispense_records",
    "doctors",
    "drugs",
    "knowledge_chunks",
    "llm_call_logs",
    "medical_records",
    "payment_orders",
    "prescriptions",
    "prescription_items",
    "rag_query_logs",
    "reports",
    "tokens",
    "users",
}


def _baseline_metadata_tables():
    from app.db.models import Base
    import app.models  # noqa: F401

    metadata_tables = {table.name for table in Base.metadata.sorted_tables}
    if metadata_tables != BASELINE_TABLES:
        missing = sorted(BASELINE_TABLES - metadata_tables)
        unexpected = sorted(metadata_tables - BASELINE_TABLES)
        raise RuntimeError(
            "Initial migration metadata does not match its frozen table list: "
            f"missing={missing}, unexpected={unexpected}. "
            "Create a new Alembic revision instead of editing this baseline."
        )
    return Base.metadata.sorted_tables


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    bind = op.get_bind()
    for table in _baseline_metadata_tables():
        table.create(bind=bind, checkfirst=False)


def downgrade() -> None:
    bind = op.get_bind()
    for table in reversed(_baseline_metadata_tables()):
        table.drop(bind=bind, checkfirst=False)
