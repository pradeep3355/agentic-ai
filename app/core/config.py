from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    VERSION: str
    API_V1_STR: str
    QDRANT_API_KEY: str
    QDRANT_URL: str
    OPENAI_API_KEY: str

    # PostgreSQL settings
    POSTGRES_PORT: int
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
