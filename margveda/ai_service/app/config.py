"""AI service settings — reads from environment variables, then .env file."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv(Path(__file__).resolve().parents[1] / ".env")


class Settings:
    # ── Service ───────────────────────────────────────────────────────────────
    SERVICE_NAME: str = "careerbrownie-ai"
    VERSION: str = "2.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    PORT: int = int(os.getenv("PORT", "9000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # ── Ollama (primary LLM — local development) ──────────────────────────────
    # Set OLLAMA_URL to empty string to skip Ollama and go straight to Claude.
    # Run locally: `ollama serve` then `ollama pull qwen2.5:7b`
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

    # ── Anthropic Claude (fallback LLM — production) ──────────────────────────
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    # Valid models: claude-sonnet-4-20250514, claude-3-5-haiku-20241022, claude-3-opus-20240229
    CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")

    # ── Shared LLM settings ────────────────────────────────────────────────────
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "1200"))
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.35"))
    LLM_TIMEOUT_SECS: int = int(os.getenv("LLM_TIMEOUT_SECS", "60"))
    LLM_MAX_RETRIES: int = int(os.getenv("LLM_MAX_RETRIES", "3"))

    # ── Embeddings (sentence-transformers, CPU-safe) ───────────────────────────
    EMBED_MODEL: str = os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")
    EMBED_DEVICE: str = os.getenv("EMBED_DEVICE", "cpu")
    EMBED_BATCH_SIZE: int = int(os.getenv("EMBED_BATCH_SIZE", "64"))
    EMBED_DIM: int = int(os.getenv("EMBED_DIM", "384"))   # all-MiniLM-L6-v2 → 384

    # ── ChromaDB (local vector store) ─────────────────────────────────────────
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

    # ── Qdrant vector database ────────────────────────────────────────────────
    # ":memory:" → in-process Qdrant (no Docker, perfect for dev)
    # "http://localhost:6333" → local Docker
    # "https://xxx.qdrant.io" → Qdrant Cloud
    QDRANT_URL: str = os.getenv("QDRANT_URL", ":memory:")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "careerbrownie_knowledge")

    # ── Retrieval ─────────────────────────────────────────────────────────────
    RETRIEVAL_TOP_K: int = int(os.getenv("RETRIEVAL_TOP_K", "6"))
    RETRIEVAL_MIN_SCORE: float = float(os.getenv("RETRIEVAL_MIN_SCORE", "0.20"))
    MAX_CONTEXT_CHARS: int = int(os.getenv("MAX_CONTEXT_CHARS", "3500"))
    CITATION_CHUNK_SIZE: int = int(os.getenv("CITATION_CHUNK_SIZE", "256"))

    # ── Chunking ──────────────────────────────────────────────────────────────
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "512"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "80"))

    # ── Redis cache (optional) ────────────────────────────────────────────────
    # Leave empty to use in-memory LRU cache instead.
    REDIS_URL: str = os.getenv("REDIS_URL", "")
    CACHE_TTL_SECS: int = int(os.getenv("CACHE_TTL_SECS", "3600"))   # 1 hour
    CACHE_MAX_MEMORY: int = int(os.getenv("CACHE_MAX_MEMORY", "500"))  # entries

    # ── Service-to-service auth ────────────────────────────────────────────────
    INTERNAL_API_KEY: str = os.getenv("INTERNAL_API_KEY", "change-me-in-production")

    # ── CORS ──────────────────────────────────────────────────────────────────
    CORS_ORIGINS: list[str] = [
        o.strip()
        for o in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://127.0.0.1:3000,"
            "http://localhost:8000,http://127.0.0.1:8000",
        ).split(",")
        if o.strip()
    ]

    # ── Derived helpers ────────────────────────────────────────────────────────
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def llm_available(self) -> bool:
        return bool(self.ANTHROPIC_API_KEY) or bool(self.OLLAMA_URL)

    @property
    def qdrant_in_memory(self) -> bool:
        return self.QDRANT_URL == ":memory:"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
