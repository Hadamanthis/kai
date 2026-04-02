from memory.models import Memory
from memory.repository import MemoryRepository

def test_save_memory(db):
    repo = MemoryRepository(db)
    repo.save(Memory(content="Isso é um teste.", session_id="teste_01"))

    saved = repo.get_all()

    # Foi salvo (existe no banco)
    assert len(saved) == 1

    # Conteúdo correto
    assert saved[0].content == "Isso é um teste."

def test_search_memory(db):
    repo = MemoryRepository(db)
    repo.save(Memory(content="Isso é um teste.", session_id="teste_01"))

    saved = repo.get_all()

    # Foi salvo (existe no banco)
    assert len(saved) == 1