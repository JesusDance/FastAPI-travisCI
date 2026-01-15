from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TESTING: bool = False
    DATABASE_URL: str = "sqlite:///db.sqlite"
    JWT_SECRET_KEY: str = "secret_key"


class TestingConfig(Settings):
    TESTING: bool = True
    DATABASE_URL: str = "sqlite:///test.db"


