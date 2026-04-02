from core.settings import settings

def test_settings_load_groq_api_key():
    assert settings.groq_api_key is not None
    assert len(settings.groq_api_key) > 0

def test_settings_load_database_url():
    assert settings.database_url is not None
    assert settings.database_url.startswith("postgresql://")