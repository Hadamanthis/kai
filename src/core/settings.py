from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    groq_api_key: str
    database_url: str
    test_database_url: str


settings = Settings()