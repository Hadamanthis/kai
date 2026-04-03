import integrations.telegram.bot as telegram_bot
from sqlalchemy import create_engine
from memory.models import Base
from core.settings import settings

if __name__ == "__main__":
    engine = create_engine(settings.database_url)
    Base.metadata.create_all(engine)

    telegram_bot.create_bot(settings.telegram_bot_token).run_polling()