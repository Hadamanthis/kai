import integrations.telegram.bot as telegram_bot
from core.settings import settings

if __name__ == "__main__":
    telegram_bot.create_bot(settings.telegram_bot_token).run_polling()