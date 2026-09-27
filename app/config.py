"""
Application configuration, loaded from environment variables (via a
.env file in development). Centralizing settings here means the Week 2
swap from SQLite to Postgres touches this one file, not a grep across
the codebase.
"""

from pydantic_settings import BaseSettings
'''
classes from pydrantic are used to authenticate app configurations
'''



class Settings(BaseSettings):
    database_url: str = "sqlite:///./flagforge.db"

    class Config:
        env_file = ".env"


settings = Settings()