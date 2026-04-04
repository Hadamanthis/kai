from conversation.graph import create_graph
from conversation.state import KaiState
from core.llm_client import LLMClient
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from memory.repository import MemoryRepository
from memory.service import MemoryService
from core.embeddings import EmbeddingClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from core.settings import settings

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        graph = context.bot_data["graph"]

        session_id = str(update.effective_chat.id)

        state = await graph.ainvoke(KaiState(session_id=session_id, user_message=update.message.text))

        await update.message.reply_text(state["response"])

    except Exception as e:
        await update.message.reply_text("Desculpe, ocorreu um erro. Tente novamente.")

def create_bot(token: str, graph) -> ApplicationBuilder:
    app = ApplicationBuilder().token(token).build()
    app.bot_data["graph"] = graph
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    return app