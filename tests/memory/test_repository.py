from core.embeddings import EmbeddingClient
from memory.models import Memory
from memory.repository import MemoryRepository

def test_save_memory(db, embedding_client):
    repo = MemoryRepository(db)

    new_memory = Memory(content="Isso é um teste.", session_id="teste_01")
    new_memory.embedding = embedding_client.embed(new_memory.content)

    repo.save(new_memory)

    saved = repo.get_all()

    # Foi salvo (existe no banco)
    assert len(saved) == 1

    # Conteúdo correto
    assert saved[0].content == "Isso é um teste."

def test_search_memory(db, embedding_client):
    repo = MemoryRepository(db)

    new_memory = Memory(content="Isso é um teste.", session_id="teste_01")
    new_memory.embedding = embedding_client.embed(new_memory.content)

    repo.save(new_memory)

    saved = repo.get_all()

    # Foi salvo (existe no banco)
    assert len(saved) == 1