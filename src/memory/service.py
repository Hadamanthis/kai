from core.embeddings import EmbeddingClient
from memory.models import Memory
from memory.repository import MemoryRepository


class MemoryService:
    def __init__(self, memory_repository: MemoryRepository, embedding_client: EmbeddingClient = None):
        self.memory_repository = memory_repository
        self.embedding_client = embedding_client or EmbeddingClient()

    def save(self, memory: Memory) -> Memory:
        memory.embedding = self.embedding_client.embed(memory.content)
        return self.memory_repository.save(memory)

    def get_all(self) -> list[Memory]:
        return self.memory_repository.get_all()
    
    def search(self, message: str, limit: int = 5) -> list[Memory]:
        embeddings = self.embedding_client.embed(message)
        return self.memory_repository.search(embeddings, limit)