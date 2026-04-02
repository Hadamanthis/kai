from conversation.graph import create_graph
from conversation.state import KaiState
from core.llm_client import LLMClient
from pydantic import BaseModel
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    llm_client = LLMClient()

    graph = create_graph(llm_client)

    state = graph.invoke(KaiState(session_id=update.effective_chat.id, user_message=update.message.text))

    await update.message.reply_text(state["response"])

def create_bot(token: str) -> ApplicationBuilder:
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    return app