from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from memory.models import Memory

class MemoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, new_memory: Memory) -> Memory:
        
        self.db.add(new_memory)
        self.db.commit()

        self.db.refresh(new_memory) # Garante que o id e os campos estão atualizados

        return new_memory
    
    def get_all(self) -> list[Memory]:
        return self.db.execute(select(Memory)).scalars().all()
    
    def search(self, embedding: list[float], username: str, limit: int) -> list[Memory]:
        results = self.db.execute(
            select(Memory)
            .order_by(Memory.embedding.cosine_distance(embedding))
            .where(Memory.username == username)
            .limit(limit)
        ).scalars().all()

        return list(results)
    
    def exists_similar(self, embedding: list[float], username: str, threshold: float = 0.15) -> bool:
        results = self.db.execute(
            select(Memory)
            .where(Memory.embedding.cosine_distance(embedding) < threshold)
            .where(Memory.username == username)
            .limit(1)
        ).scalars().all()

        return len(results) > 0

    def delete(self, memory_id: int) -> None:
        result = self.db.execute(
            select(Memory)
            .where(Memory.id == memory_id)
        ).scalars().one_or_none()

        if result:
            self.db.delete(result)
            self.db.commit()
    
    def get_all_by_username(self, username: str) -> list[Memory]:
        result = self.db.execute(
            select(Memory)
            .where(Memory.username == username)
        ).scalars().all()

        return result