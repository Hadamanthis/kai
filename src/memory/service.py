from memory.models import Memory
from memory.repository import MemoryRepository


class MemoryService:
    def __init__(self, memory_repository: MemoryRepository):
        self.memory_repository = memory_repository

    def save(self, memory: Memory) -> Memory:
        return self.memory_repository.save(memory)

    def get_all(self) -> list[Memory]:
        return self.memory_repository.get_all()