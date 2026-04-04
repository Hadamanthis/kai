from conversation.graph import create_graph
from conversation.state import KaiState
from fastapi import Request
from fastapi.routing import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    user_message: str

class ChatResponse(BaseModel):
    content: str

@router.post("/chat")
async def chat(req: Request, request: ChatRequest) -> ChatResponse:
    graph = req.app.state.graph

    initial_state = KaiState(session_id=request.session_id, user_message=request.user_message)

    state = await graph.ainvoke(initial_state)

    return ChatResponse(content=state["response"])