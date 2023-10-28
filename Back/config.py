import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    github_oath_client_id: str = os.environ["GITHUB_OAUTH_CLIENT_ID"]
    github_oath_client_secret: str = os.environ["GITHUB_OAUTH_CLIENT_SECRET"]

    openai_api_key: str = os.environ["OPENAI_API_KEY"]

    cors_origins: list[str] = [
        "https://localhost:9000",
    ]

settings = Settings()