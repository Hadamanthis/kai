from conversation.state import KaiState
from conversation.graph import create_graph
from core.embeddings import EmbeddingClient
from core.llm_client import LLMClient
from fastapi.routing import APIRouter
from memory.repository import MemoryRepository
from memory.service import MemoryService
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.engine import create_engine
from core.settings import settings

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    user_message: str

class ChatResponse(BaseModel):
    content: str

@router.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    memory_repository = MemoryRepository(Session(create_engine(settings.database_url)))
    memory_service = MemoryService(memory_repository)
    
    llm_client = LLMClient()

    graph = create_graph(llm_client, memory_service)

    initial_state = KaiState(session_id=request.session_id, user_message=request.user_message)

    state = await graph.ainvoke(initial_state)

    return ChatResponse(content=state["response"])