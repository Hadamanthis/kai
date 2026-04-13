from core.embeddings import EmbeddingClient
from memory.models import Memory
from memory.repository import MemoryRepository


class MemoryService:
    def __init__(self, memory_repository: MemoryRepository, embedding_client: EmbeddingClient = None):
        self.memory_repository = memory_repository
        self.embedding_client = embedding_client or EmbeddingClient()

    def save(self, memory: Memory) -> Memory | None:
        memory.embedding = self.embedding_client.embed(memory.content)

        if self.memory_repository.exists_similar(memory.embedding, memory.username):
            return None

        return self.memory_repository.save(memory)

    def get_all(self) -> list[Memory]:
        return self.memory_repository.get_all()
    
    def search(self, message: str, username: str, limit: int = 5) -> list[Memory]:
        embeddings = self.embedding_client.embed(message)
        return self.memory_repository.search(embeddings, username, limit)
    
    def delete(self, memory_id: str) -> None:
        self.memory_repository.delete(memory_id)

    def get_all_by_username(self, username: str) -> list[Memory]:
        return self.memory_repository.get_all_by_username(username)