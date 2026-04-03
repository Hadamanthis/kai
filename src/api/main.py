from fastapi import FastAPI
from conversation.routes import router
import uvicorn
from sqlalchemy import create_engine
from memory.models import Base
from core.settings import settings

app = FastAPI()

app.include_router(router, prefix="/api")

engine = create_engine(settings.database_url)
Base.metadata.create_all(engine)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)