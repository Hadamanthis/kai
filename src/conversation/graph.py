from conversation.nodes import make_respond
from conversation.state import KaiState
from core.llm_client import LLMClient
from langgraph.graph import StateGraph, START, END

def create_graph(llm_client: LLMClient):
    graph = StateGraph(KaiState)

    graph.add_node("respond", make_respond(llm_client))

    graph.add_edge(START, "respond")
    graph.add_edge("respond", END)

    return graph.compile()