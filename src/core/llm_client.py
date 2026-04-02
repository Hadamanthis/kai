from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage
from core.settings import settings
from typing import TypeVar

T = TypeVar("T")

class LLMClient:
    def __init__(self):
        self.model = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            api_key=settings.groq_api_key
        )
    
    def call(self, messages: list[BaseMessage]):
        return self.model.invoke(messages).content
    
    def call_structured(self, messages: list[BaseMessage], schema: type[T]) -> T:
        structured_llm = self.model.with_structured_output(schema)
        return structured_llm.invoke(messages).content
