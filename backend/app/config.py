from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://demo:demo@db:5432/demo"


settings = Settings()
