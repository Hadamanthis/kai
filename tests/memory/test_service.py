from core.embeddings import EmbeddingClient
from memory.models import Memory
from memory.repository import MemoryRepository
from memory.service import MemoryService

def test_service_save_memory(db, embedding_client):
    repository = MemoryRepository(db)
    service = MemoryService(repository, embedding_client)

    memory = Memory(content="Gosta de Python.", session_id="test_01")
    response = service.save(memory)

    assert response is not None

    assert response.content == "Gosta de Python."

def test_service_get_all_memory(db, embedding_client):
    repository = MemoryRepository(db)
    service = MemoryService(repository, embedding_client)
    
    service.save(Memory(content="Gosta de Python.", session_id="test_01"))
    service.save(Memory(content="Gosta de IA.", session_id="test_01"))

    memories = service.get_all()

    assert len(memories) == 2

    assert memories[0].content == "Gosta de Python."

def test_service_search_memory(db, embedding_client):
    repository = MemoryRepository(db)
    service = MemoryService(repository, embedding_client)

    memory1 = Memory(content="Programação é muito legal.", session_id="teste_01")
    service.save(memory1)
    service.save(Memory(content="Carros de corrida são os melhores.", session_id="teste_01"))

    memories = service.search("Amanhã eu irei programar.", limit=1)

    assert len(memories) == 1
    assert memories[0].content == "Programação é muito legal."


        