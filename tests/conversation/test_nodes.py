from unittest.mock import MagicMock, patch
from conversation.nodes import respond, retrieve_memory, memorize
from conversation.state import KaiState
from core.llm_client import LLMClient
from memory.models import Memory
from user.service import UserService

def make_state(**kwargs) -> KaiState:
    defaults = {
        "session_id": "test_session",
        "username": "test_username",
        "user_message": "Eu gosto de Python.",
        "relevant_memories": [],
        "response": ""
    }
    return KaiState(**{**defaults, **kwargs})

def make_respond_services() -> tuple[MagicMock, MagicMock]:
    llm_client = MagicMock()
    llm_client.call.return_value = "Resposta do modelo"

    user_service = MagicMock()
    user = MagicMock()
    user.name, user.bio, user.age = "test_user", "user_bio", 42
    user_service.get_by_username.return_value = user

    return llm_client, user_service

def test_respond_calls_lmm_and_set_response():
    llm_client, user_service = make_respond_services()

    initial_state = make_state(relevant_memories=["Usuário gosta de café"])
    final_state = respond(llm_client, user_service)(initial_state)

    llm_client.call.assert_called_once()
    user_service.get_by_username.assert_called_once_with(initial_state["username"])
    assert final_state["response"] == "Resposta do modelo"

def test_respond_with_empty_memories():
    llm_client, user_service = make_respond_services()

    initial_state = make_state(relevant_memories=[])
    final_state = respond(llm_client, user_service)(initial_state)

    llm_client.call.assert_called_once()
    user_service.get_by_username.assert_called_once_with(initial_state["username"])
    assert final_state["response"] == "Resposta do modelo"

def test_retrieve_memory_populates_relevant_memories():
    memory_service = MagicMock()
    memory_service.search.return_value = [
        Memory(content="usuário gosta de Python", username="test_username", session_id="test_session"),
        Memory(content="usuário não sabe cozinhar", username="test_username", session_id="test_session"),
    ]

    initial_state = make_state()
    final_state = retrieve_memory(memory_service)(initial_state)

    memory_service.search.assert_called_once_with("Eu gosto de Python.", "test_username")
    assert final_state["relevant_memories"] == ["usuário gosta de Python", "usuário não sabe cozinhar"]

def test_retrieve_memory_empty_result():
    memory_service = MagicMock()
    memory_service.search.return_value = []

    initial_state = make_state()
    final_state = retrieve_memory(memory_service)(initial_state)

    assert final_state["relevant_memories"] == []

def test_memorize_saves_extracted_facts():
    extracted = MagicMock()
    extracted.facts = ["usuário gosta de Python", "usuário não sabe cozinhar"]
    llm_client = MagicMock()
    llm_client.call_structured.return_value = extracted

    memory_service = MagicMock()
    
    initial_state = make_state()
    memorize(llm_client, memory_service)(initial_state)

    assert memory_service.save.call_count == 2

    saved_contents = [call.args[0].content for call in memory_service.save.call_args_list]
    assert "usuário gosta de Python" in saved_contents
    assert "usuário não sabe cozinhar" in saved_contents

def test_memorize_saves_nothing_when_no_facts():
    extracted = MagicMock()
    extracted.facts = []
    llm_client = MagicMock()
    llm_client.call_structured.return_value = extracted
    memory_service = MagicMock()

    state = make_state()
    memorize(llm_client, memory_service)(state)

    memory_service.save.assert_not_called()