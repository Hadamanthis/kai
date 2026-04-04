from conversation.graph import create_graph
from core.embeddings import EmbeddingClient
from core.llm_client import LLMClient
import integrations.telegram.bot as telegram_bot
from memory.repository import MemoryRepository
from memory.service import MemoryService
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from core.settings import settings

if __name__ == "__main__":
    # Inicializa a conexão com o banco
    engine = create_engine(settings.database_url)
    session = Session(engine)

    memory_service = MemoryService(MemoryRepository(session), EmbeddingClient())
    graph = create_graph(LLMClient(), MemoryService)

    app = telegram_bot.create_bot(settings.telegram_bot_token, graph)
    
    try:
        app.run_polling()
    finally:
        session.close()
        engine.close()