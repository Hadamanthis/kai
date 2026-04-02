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