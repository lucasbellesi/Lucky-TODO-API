import os
from pathlib import Path
from dotenv import load_dotenv


# Load .env located in the package root (python-api/.env) if present
_env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=_env_path if _env_path.exists() else None)


class Settings:
    def __init__(self) -> None:
        # Database
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./todo.db")
        # Auth
        self.SECRET_KEY: str = os.getenv("SECRET_KEY", "secret")
        try:
            self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
        except ValueError:
            self.ACCESS_TOKEN_EXPIRE_MINUTES = 30


settings = Settings()

