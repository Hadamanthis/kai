import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from memory.models import Base, Memory
from memory.repository import MemoryRepository
from core.settings import settings

@pytest.fixture
def db():
    engine = create_engine(settings.test_database_url)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)

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