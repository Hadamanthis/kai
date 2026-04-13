from contextlib import asynccontextmanager
from core.embeddings import EmbeddingClient
from core.llm_client import LLMClient
from fastapi import FastAPI
from conversation.routes import router
from memory.repository import MemoryRepository
from memory.service import MemoryService
from user.repository import UserRepository
from user.service import UserService
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from core.settings import settings
from conversation.graph import create_graph

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa a conexão com o banco
    engine = create_engine(settings.database_url)
    session = Session(engine)

    user_service = UserService(UserRepository(session))
    memory_service = MemoryService(MemoryRepository(session), EmbeddingClient())
    app.state.graph = create_graph(LLMClient(), memory_service, user_service)
    app.state.memory_service = memory_service
    app.state.user_service = user_service
    
    yield

    session.close()
    engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)