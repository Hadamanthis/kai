from sqlalchemy import select
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
    
    def search(self, embedding: list[float], limit: int) -> list[Memory]:
        results = self.db.execute(
            select(Memory)
            .order_by(Memory.embedding.cosine_distance(embedding))
            .limit(limit)
        ).scalars().all()

        return list(results)
    
    def exists_similar(self, embedding: list[float], threshold: float = 0.15) -> bool:
        results = self.db.execute(
            select(Memory)
            .where(Memory.embedding.cosine_distance(embedding) < threshold)
            .limit(1)
        ).scalars().all()

        return len(results) > 0