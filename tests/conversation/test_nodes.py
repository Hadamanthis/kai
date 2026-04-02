from conversation.state import KaiState
from conversation.nodes import make_respond
from core.llm_client import LLMClient

def test_node_response(db):
    kai_state = KaiState(session_id="test_01", user_message="Eu amo Python.")

    llm_client = LLMClient()

    respond = make_respond(llm_client)

    upd_kai_state = respond(kai_state)

    assert upd_kai_state["response"] is not None