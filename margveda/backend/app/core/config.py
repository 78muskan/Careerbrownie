import os
from functools import lru_cache
from pathlib import Path


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


def _parse_cors_origins(value: str) -> list[str]:
    return [origin.strip() for origin in value.split(",") if origin.strip()]


class Settings:
    def __init__(self) -> None:
        backend_dir = Path(__file__).resolve().parents[2]
        _load_env_file(backend_dir / ".env")

        self.PROJECT_NAME = os.getenv("PROJECT_NAME", "Career Brownie API")
        self.VERSION = os.getenv("VERSION", "1.0.0")
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
        self.API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./margveda.db")
        self.AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://127.0.0.1:9000")
        self.SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
        self.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440")
        )
        self.BACKEND_CORS_ORIGINS = _parse_cors_origins(
            os.getenv(
                "BACKEND_CORS_ORIGINS",
                "http://localhost:3000,http://127.0.0.1:3000,"
                "http://localhost:5173,http://127.0.0.1:5173,"
                "http://localhost:8000,http://127.0.0.1:8000",
            )
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
