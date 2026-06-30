from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path


class Settings:
    # Service
    SERVICE_NAME: str = "careerbrownie-ai"
    VERSION: str = "2.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    PORT: int = int(os.getenv("PORT", "9000"))

    # Ollama (LLM)
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
    OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", "120"))
    OLLAMA_MAX_TOKENS: int = int(os.getenv("OLLAMA_MAX_TOKENS", "1024"))
    OLLAMA_TEMPERATURE: float = float(os.getenv("OLLAMA_TEMPERATURE", "0.3"))

    # Embeddings
    EMBED_MODEL: str = os.getenv("EMBED_MODEL", "BAAI/bge-m3")
    EMBED_DEVICE: str = os.getenv("EMBED_DEVICE", "cpu")  # cpu | cuda
    EMBED_BATCH_SIZE: int = int(os.getenv("EMBED_BATCH_SIZE", "32"))
    EMBED_MAX_LENGTH: int = int(os.getenv("EMBED_MAX_LENGTH", "8192"))

    # Reranker
    RERANKER_MODEL: str = os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-v2-m3")
    RERANKER_TOP_K: int = int(os.getenv("RERANKER_TOP_K", "5"))

    # Qdrant
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    QDRANT_DENSE_DIM: int = 1024  # bge-m3 dense dimension

    # Collection names
    COLLECTION_CAREERS: str = "careers"
    COLLECTION_COLLEGES: str = "colleges"
    COLLECTION_SCHOLARSHIPS: str = "scholarships"
    COLLECTION_EXAMS: str = "entrance_exams"
    COLLECTION_FAQS: str = "faqs"
    COLLECTION_ROADMAPS: str = "roadmaps"

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/1")
    MEMORY_TTL: int = int(os.getenv("MEMORY_TTL", "86400"))  # 24h
    MEMORY_MAX_TURNS: int = int(os.getenv("MEMORY_MAX_TURNS", "20"))

    # RAG
    RAG_RETRIEVE_TOP_K: int = int(os.getenv("RAG_RETRIEVE_TOP_K", "20"))
    RAG_RERANK_TOP_K: int = int(os.getenv("RAG_RERANK_TOP_K", "5"))
    RAG_DENSE_WEIGHT: float = float(os.getenv("RAG_DENSE_WEIGHT", "0.7"))
    RAG_SPARSE_WEIGHT: float = float(os.getenv("RAG_SPARSE_WEIGHT", "0.3"))
    RAG_CACHE_TTL: int = int(os.getenv("RAG_CACHE_TTL", "3600"))

    # Auth (service-to-service)
    INTERNAL_API_KEY: str = os.getenv("INTERNAL_API_KEY", "change-me-in-production")

    # Fallback (Anthropic — used only if Ollama unavailable)
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL: str = "claude-sonnet-4-6"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
