from conversation.graph import create_graph
from conversation.state import KaiState
from core.llm_client import LLMClient
from pydantic import BaseModel
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        llm_client = LLMClient()

        graph = create_graph(llm_client)

        telegram_chat_id = str(update.effective_chat.id)

        state = await graph.ainvoke(KaiState(session_id=telegram_chat_id, user_message=update.message.text))

        await update.message.reply_text(state["response"])

    except Exception as e:
        await update.message.reply_text("Desculpe, ocorreu um erro. Tente novamente.")

def create_bot(token: str) -> ApplicationBuilder:
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    return app