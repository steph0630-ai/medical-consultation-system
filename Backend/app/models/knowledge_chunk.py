from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import TSVECTOR

from app.models.base import BaseModel


class KnowledgeChunk(BaseModel):
    __tablename__ = "knowledge_chunks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    source = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1024), nullable=False)
    chunk_metadata = Column("metadata", JSON, nullable=True)
    content_tsv = Column(TSVECTOR, nullable=True)
