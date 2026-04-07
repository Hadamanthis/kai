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
                Extraia APENAS fatos pessoais sobre o usuário que ele explicitamente declarou sobre si mesmo. 
                Exemplos válidos: 'usuário gosta de café', 'usuário mora em Fortaleza'
                Exemplos inválidos: tópicos perguntados, assuntos da conversa, inferências. "
                Se a mensagem for uma pergunta ou não contiver fatos pessoais, retorne lista vazia."""),
            ("human", "{user_message}")
        ])

        messages = messages_template.invoke({
            "user_message": state["user_message"]
        })
        
        result = llm_client.call_structured(messages, ExtractedFacts)

        for facts in result.facts:
            new_memory = Memory(
                content=facts,
                session_id=state["session_id"],
                username=state["username"]
            )
            memory_service.save(new_memory)
        
        return state
    
    return _memorize