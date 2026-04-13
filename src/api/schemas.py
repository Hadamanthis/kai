from pydantic import BaseModel

# User
class UserCreateRequest(BaseModel):
    username: str
    name: str
    bio: str | None = None
    age: int | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    bio: str | None = None
    age: int | None = None

    model_config = {"from_attributes": True}

# Memory
class MemoryResponse(BaseModel):
    id: int
    content: str
    username: str
    session_id: str

    model_config = {"from_attributes": True}

# Chat
class ChatRequest(BaseModel):
    session_id: str
    username: str
    user_message: str

class ChatResponse(BaseModel):
    content: str