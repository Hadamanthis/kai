from conversation.state import KaiState
from conversation.graph import create_graph
from core.llm_client import LLMClient
from fastapi.routing import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    user_message: str

class ChatResponse(BaseModel):
    content: str

@router.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    llm_client = LLMClient()

    graph = create_graph(llm_client)

    initial_state = KaiState(session_id=request.session_id, user_message=request.user_message)

    state = await graph.ainvoke(initial_state)

    return ChatResponse(content=state["response"])