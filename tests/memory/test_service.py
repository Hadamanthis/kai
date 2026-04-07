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

    memory = Memory(content="Gosta de Python.", username="teste_01", session_id="test_01")
    memory_repository.save.return_value = memory
    memory_repository.exists_similar.return_value = False

    result = memory_service.save(memory)

    embedding_client.embed.assert_called_once_with(memory.content)
    memory_repository.save.assert_called_once_with(memory)

    assert result.content == "Gosta de Python."

def test_service_get_all_memory():
    memory_service, memory_repository, _ = make_service()
    memory_repository.get_all.return_value = [
        Memory(content="Gosta de Python.", username="teste_01", session_id="test_01"),
        Memory(content="Gosta de IA.", username="teste_01", session_id="test_01"),
    ]

    memories = memory_service.get_all()

    memory_repository.get_all.assert_called_once()
    assert len(memories) == 2

def test_service_semantic_search_memory():
    memory_service, memory_repository, embedding_client = make_service()
    memory_repository.search.return_value = [
        Memory(content="Programação é muito legal.", username="teste_01", session_id="teste_01")
    ]

    memories = memory_service.search("Amanhã eu irei programar.", "teste_01", limit=1)

    embedding_client.embed.assert_called_once_with("Amanhã eu irei programar.")
    memory_repository.search.assert_called_once_with("embedding_value", "teste_01", 1)

    assert memories[0].content == "Programação é muito legal."


def test_service_not_save_duplicated_memory():
    memory_service, memory_repository, embedding_client = make_service()
    memory_repository.exists_similar.return_value = True

    saved_memory = memory_service.save(Memory(content="Gosta de Python.", username="teste_01", session_id="test_01"))

    assert saved_memory == None
    memory_repository.exists_similar.assert_called_once()
    memory_repository.save.assert_not_called()