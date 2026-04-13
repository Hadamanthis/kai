from core.embeddings import EmbeddingClient
from memory.models import Memory
from memory.repository import MemoryRepository

def make_memory(emb_cli: EmbeddingClient, content = "Isso é um teste.", username="username", session_id="teste_01"):
    memory = Memory(content=content, username=username, session_id=session_id)
    memory.embedding = emb_cli.embed(memory.content)
    return memory

def test_repository_save_memory(db, embedding_client):
    repo = MemoryRepository(db)

    new_memory = make_memory(embedding_client)

    repo.save(new_memory)

    saved = repo.get_all()

    # Foi salvo (existe no banco)
    assert len(saved) == 1

    # Conteúdo correto
    assert saved[0].content == new_memory.content

def test_repository_get_all_memory(db, embedding_client):
    repo = MemoryRepository(db)

    new_memory = make_memory(embedding_client)

    repo.save(new_memory)

    saved = repo.get_all()

    # Foi salvo (existe no banco)
    assert len(saved) == 1

def test_repository_semantic_search(db, embedding_client):
    repo = MemoryRepository(db)

    # Deve ser retornada por semântica
    new_memory1 = make_memory(embedding_client, content="Programação é muito legal.", username='teste_01')
    # Não deve ser retornada por username diferente
    new_memory2 = make_memory(embedding_client, content="Gosto de programar.", username='teste_02')
    # Não deve ser retornado por semântica diferente
    new_memory3 = make_memory(embedding_client, content="Carros de corrida são os melhores.", username='teste_01')

    repo.save(new_memory1)
    repo.save(new_memory2)
    repo.save(new_memory3)
    
    emb_to_search = embedding_client.embed('Gosto de programar.')

    memories = repo.search(emb_to_search, 'teste_01', limit=1)

    assert len(memories) == 1

    assert memories[0].content == new_memory1.content

def test_exists_similar(db, embedding_client):
    repo = MemoryRepository(db)

    # Salvando uma memória
    new_memory = make_memory(embedding_client, content="Programação é muito legal.")
    repo.save(new_memory)

    different_embedding = embedding_client.embed("Gosto de café.")

    assert repo.exists_similar(new_memory.embedding, new_memory.username, 0.15) == True
    assert repo.exists_similar(different_embedding, new_memory.username, 0.15) == False

def test_repository_get_all_by_username(db, embedding_client):
    repo = MemoryRepository(db)

    m1 = Memory(content="Gosta de Python.", session_id="s1", username="alice")
    m1.embedding = embedding_client.embed(m1.content)
    m2 = Memory(content="Gosta de café.", session_id="s1", username="alice")
    m2.embedding = embedding_client.embed(m2.content)
    m3 = Memory(content="Gosta de surf.", session_id="s1", username="bob")
    m3.embedding = embedding_client.embed(m3.content)

    repo.save(m1)
    repo.save(m2)
    repo.save(m3)

    results = repo.get_all_by_username("alice")

    assert len(results) == 2
    assert all(m.username == "alice" for m in results)


def test_repository_delete_memory(db, embedding_client):
    repo = MemoryRepository(db)

    m = Memory(content="Gosta de Python.", session_id="s1", username="alice")
    m.embedding = embedding_client.embed(m.content)
    repo.save(m)

    assert len(repo.get_all()) == 1

    repo.delete(m.id)

    assert len(repo.get_all()) == 0