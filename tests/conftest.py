from core.embeddings import EmbeddingClient
import pytest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from memory.models import Base
from core.settings import settings

@pytest.fixture
def db():
    engine = create_engine(settings.test_database_url)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)

@pytest.fixture(scope="session")
def embedding_client():
    return EmbeddingClient()