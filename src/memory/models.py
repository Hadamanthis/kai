from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from core.models import Base
from pgvector.sqlalchemy import Vector

class Memory(Base):
    __tablename__ = "memories"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String)
    session_id: Mapped[str] = mapped_column(String)
    embedding: Mapped[list[float]] = mapped_column(Vector(384))
    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())