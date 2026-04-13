import json
from typing import Callable

from conversation.state import KaiState
from core.llm_client import LLMClient
from memory.service import MemoryService
from memory.models import Memory
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from user.service import UserService


def respond(llm_client: LLMClient, user_service: UserService) -> Callable[[KaiState], KaiState]:

    def _respond(state: KaiState) -> KaiState:

        memories_context = "\n".join(state["relevant_memories"])

        messages_template = ChatPromptTemplate([
            ("system", """
                Você é o Kai, um assistente pessoal do usuário.
             
                Use as informações do usuário e as memórias relevantes para respondê-lo.
                Não invente informações, se não tiver a informação diga que não sabe.

                Perfil de usuário:
                - Nome: {user_name}
                - Bio: {user_bio}
                - Idade: {user_age}
             
                Memórias relevantes:
                {memories_context}
            """),
            ("human", "{user_message}")
        ])

        user = user_service.get_by_username(state["username"])

        messages = messages_template.invoke({
            "user_name": user.name if user else "Usuário",
            "user_bio": user.bio if user else "Não informado",
            "user_age": user.age if user else "Não informado",
            "memories_context": memories_context,
            "user_message": state["user_message"]
        })

        state["response"] = llm_client.call(messages)

        return state
    
    return _respond

def retrieve_memory(memory_service: MemoryService) -> Callable[[KaiState], KaiState]:

    def _retrieve_memory(state: KaiState):
        memory_list = memory_service.search(state["user_message"], state["username"]) # list[Memory]
        state["relevant_memories"] = [memory.content for memory in memory_list] or [] # list[str]
        
        return state

    return _retrieve_memory

class ExtractedFacts(BaseModel):
    facts: list[str]

def memorize(llm_client: LLMClient, memory_service: MemoryService) -> Callable[[KaiState], KaiState]:
    
    def _memorize(state: KaiState):
        messages_template = ChatPromptTemplate([
            ("system", """
            Extraia fatos relevantes sobre o usuário a partir da mensagem dele.
            Capture:
            - Interesses e hobbies mencionados
            - Objetivos e intenções expressados ("quero aprender X", "estou estudando Y")
            - Preferências e opiniões ("gosto de", "não gosto de")
            - Informações pessoais relevantes não contidas no perfil
            
            Não capture:
            - Perguntas feitas pelo usuário
            - O nome do usuário — já registrado no perfil como {user_name}
            - Inferências suas
            
            Se não houver nada relevante, retorne lista vazia.
            
            Responda APENAS com JSON válido, sem texto adicional, no formato:
            {{"facts": ["fato 1", "fato 2"]}}
            """),
            ("human", "{user_message}")
        ])

        messages = messages_template.invoke({
            "user_message": state["user_message"],
            "user_name": state["username"]
        })
        
        result = llm_client.call(messages)

        try:
            data = json.loads(result)
            facts = data.get("facts", [])
        except json.JSONDecodeError:
            facts = []

        for fact in facts:
            memory_service.save(
                Memory(
                    content=fact,
                    session_id=state["session_id"],
                    username=state["username"]
                )
            )
        
        return state
    
    return _memorize