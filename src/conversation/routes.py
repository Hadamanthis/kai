from conversation.state import KaiState
from fastapi import HTTPException, Request
from fastapi.routing import APIRouter
from memory.service import MemoryService
from user.models import User
from user.service import UserService
from api.schemas import ChatRequest, ChatResponse, UserCreateRequest, UserResponse, MemoryResponse

router = APIRouter()

@router.post("/chat")
async def chat(req: Request, request: ChatRequest) -> ChatResponse:
    graph = req.app.state.graph

    initial_state = KaiState(session_id=request.session_id, username=request.username, user_message=request.user_message)

    state = await graph.ainvoke(initial_state)

    return ChatResponse(content=state["response"])

@router.post("/user/create")
async def create_user(req: Request, request: UserCreateRequest) -> UserResponse | None:
    user_service: UserService = req.app.state.user_service

    saved_user = user_service.save(
        User(
            username=request.username,
            name=request.name,
            bio=request.bio,
            age=request.age
        )
    )

    if saved_user is None:
        raise HTTPException(status_code=409, detail="Username já existe")

    return saved_user

@router.get("/user/{username}")
async def get_by_username(req: Request, username: str) -> UserResponse:
    user_service: UserService = req.app.state.user_service

    return user_service.get_by_username(username)

@router.delete("/memories/{memory_id}", status_code=204)
async def delete_memory(req: Request, memory_id: int) -> None:
    memory_service = req.app.state.memory_service
    memory_service.delete(memory_id)

@router.get("/memories/{username}")
async def get_memories(req: Request, username: str) -> list[MemoryResponse]:
    memory_service = req.app.state.memory_service
    return memory_service.get_all_by_username(username)