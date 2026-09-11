from sqlalchemy import Column, Integer, JSON, String, Text

from app.models.base import BaseModel


class RAGQueryLog(BaseModel):
    __tablename__ = "rag_query_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_type = Column(String(50), nullable=True, index=True)
    query = Column(Text, nullable=False)
    top_k = Column(Integer, nullable=False)
    result_ids = Column(JSON, nullable=False)
    latency_ms = Column(Integer, nullable=False)
