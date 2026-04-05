from core.embeddings import EmbeddingClient
from memory.models import Memory
from memory.repository import MemoryRepository

def test_respository_save_memory(db, embedding_client):
    repo = MemoryRepository(db)

    new_memory = Memory(content="Isso é um teste.", session_id="teste_01")
    new_memory.embedding = embedding_client.embed(new_memory.content)

    repo.save(new_memory)

    saved = repo.get_all()

    # Foi salvo (existe no banco)
    assert len(saved) == 1

    # Conteúdo correto
    assert saved[0].content == "Isso é um teste."

def test_repository_get_all_memory(db, embedding_client):
    repo = MemoryRepository(db)

    new_memory = Memory(content="Isso é um teste.", session_id="teste_01")
    new_memory.embedding = embedding_client.embed(new_memory.content)

    repo.save(new_memory)

    saved = repo.get_all()

    # Foi salvo (existe no banco)
    assert len(saved) == 1

def test_repository_semantic_search(db, embedding_client):
    repo = MemoryRepository(db)

    new_memory1 = Memory(content="Programação é muito legal.", session_id="teste_01")
    new_memory1.embedding = embedding_client.embed(new_memory1.content)
    new_memory2 = Memory(content="Carros de corrida são os melhores.", session_id="teste_01")
    new_memory2.embedding = embedding_client.embed(new_memory2.content)

    repo.save(new_memory1)
    repo.save(new_memory2)
    
    emb_to_search = embedding_client.embed('Gosto de programar.')

    memories = repo.search(emb_to_search, limit=1)

    assert len(memories) == 1

    assert memories[0].content == new_memory1.content

def test_exists_similar(db, embedding_client):
    repo = MemoryRepository(db)

    # Salvando uma memória
    new_memory = Memory(content="Programação é muito legal.", session_id="teste_01")
    new_memory.embedding = embedding_client.embed(new_memory.content)
    repo.save(new_memory)

    different_embedding = embedding_client.embed("Gosto de café.")

    assert repo.exists_similar(new_memory.embedding, 0.15) == True
    assert repo.exists_similar(different_embedding, 0.15) == False
