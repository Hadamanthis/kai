from typing import Callable

from conversation.state import KaiState
from core.llm_client import LLMClient


def make_respond(llm_client: LLMClient) -> Callable[[KaiState], KaiState]:

    def respond(state: KaiState) -> KaiState:
        state["response"] = llm_client.call(state["user_message"])

        return state
    
    return respond