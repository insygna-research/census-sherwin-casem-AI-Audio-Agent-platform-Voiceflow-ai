from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str
    anthropic_api_key: str
    openai_api_key: str
    elevenlabs_api_key: str
    elevenlabs_voice_id: str
    redis_url: str
    database_url: str
    ngrok_url: str = ""
    log_level: str = "INFO"
    app_env: str = "development"
    app_port: int = 8000

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
