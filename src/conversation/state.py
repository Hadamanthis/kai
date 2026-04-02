from typing import TypedDict

class KaiState(TypedDict):
    session_id: str
    user_message: str
    response: str | None
