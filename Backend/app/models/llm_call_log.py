from sqlalchemy import Column, Integer, String, Text

from app.models.base import BaseModel


class LLMCallLog(BaseModel):
    __tablename__ = "llm_call_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_type = Column(String(50), nullable=False, index=True)
    prompt_hash = Column(String(64), nullable=True, index=True)
    input_tokens = Column(Integer, nullable=False)
    output_tokens = Column(Integer, nullable=False)
    latency_ms = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, index=True)
    error_message = Column(Text, nullable=True)
