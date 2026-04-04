from unittest.mock import MagicMock
from memory.models import Memory
from memory.service import MemoryService

def make_service():
    memory_repository = MagicMock()
    embedding_client = MagicMock()
    embedding_client.embed.return_value = "embedding_value"
    return MemoryService(memory_repository, embedding_client), memory_repository, embedding_client
    

def test_service_save_memory():
    memory_service, memory_repository, embedding_client = make_service()

    memory = Memory(content="Gosta de Python.", session_id="test_01")
    memory_repository.save.return_value = memory

    result = memory_service.save(memory)

    embedding_client.embed.assert_called_once_with(memory.content)
    memory_repository.save.assert_called_once_with(memory)

    assert result.content == "Gosta de Python."

def test_service_get_all_memory():
    memory_service, memory_repository, _ = make_service()
    memory_repository.get_all.return_value = [
        Memory(content="Gosta de Python.", session_id="test_01"),
        Memory(content="Gosta de IA.", session_id="test_01"),
    ]

    memories = memory_service.get_all()

    memory_repository.get_all.assert_called_once()
    assert len(memories) == 2

def test_service_semantic_search_memory():
    memory_service, memory_repository, embedding_client = make_service()
    memory_repository.search.return_value = [
        Memory(content="Programação é muito legal.", session_id="teste_01")
    ]

    memories = memory_service.search("Amanhã eu irei programar.", limit=1)

    embedding_client.embed.assert_called_once_with("Amanhã eu irei programar.")
    memory_repository.search.assert_called_once_with("embedding_value", 1)

    assert memories[0].content == "Programação é muito legal."


        