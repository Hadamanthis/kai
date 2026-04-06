from conversation.nodes import respond, retrieve_memory, memorize
from conversation.state import KaiState
from core.embeddings import EmbeddingClient
from core.llm_client import LLMClient
from langgraph.graph import StateGraph, START, END
from memory.service import MemoryService
from user.service import UserService

def create_graph(llm_client: LLMClient, memory_service: MemoryService, user_service: UserService):
    graph = StateGraph(KaiState)

    graph.add_node("retrieve_memory", retrieve_memory(memory_service))
    graph.add_node("respond", respond(llm_client, user_service))
    graph.add_node("memorize", memorize(llm_client, memory_service))

    graph.add_edge(START, "retrieve_memory")
    graph.add_edge("retrieve_memory", "respond")
    graph.add_edge("respond", "memorize")
    graph.add_edge("memorize", END)

    return graph.compile()