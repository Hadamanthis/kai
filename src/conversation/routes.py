from conversation.graph import create_graph
from conversation.state import KaiState
from fastapi import HTTPException, Request
from fastapi.routing import APIRouter
from pydantic import BaseModel
from user.models import User
from user.service import UserService

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    username: str
    user_message: str

class UserCreateRequest(BaseModel):
    username: str
    name: str
    bio: str | None
    age: int | None

class ChatResponse(BaseModel):
    content: str

@router.post("/chat")
async def chat(req: Request, request: ChatRequest) -> ChatResponse:
    graph = req.app.state.graph

    initial_state = KaiState(session_id=request.session_id, username=request.username, user_message=request.user_message)

    state = await graph.ainvoke(initial_state)

    return ChatResponse(content=state["response"])

@router.post("/user/create")
async def create_user(req: Request, request: UserCreateRequest) -> User | None:
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
async def get_by_username(req: Request, username: str) -> User:
    user_service: UserService = req.app.state.user_service

    return user_service.get_by_username(username)