from typing import TypedDict

class KaiState(TypedDict):
    session_id: str
    user_message: str
    relevant_memories: list[str] | None
    response: str | None
