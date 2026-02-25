from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    bot_token:SecretStr
    database:SecretStr
    redis_host:SecretStr
    redis_port:SecretStr
    redis_db:SecretStr
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

config = Settings()