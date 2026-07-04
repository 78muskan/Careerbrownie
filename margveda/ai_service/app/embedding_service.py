"""Sentence-level embedding service.

Wraps ``sentence-transformers`` with lazy model loading, batch encoding, and
L2 normalisation.  The model is loaded once on first use and cached for the
lifetime of the process.

Default model: ``all-MiniLM-L6-v2``
  - 22 M parameters, 384-dimensional vectors, ~90 MB on disk
  - No GPU required; fast enough on CPU for < 1 s per query
  - Normalised vectors → cosine similarity reduces to dot product

Override via EMBED_MODEL environment variable.
"""
from __future__ import annotations

import logging
import threading
from typing import TYPE_CHECKING

import numpy as np

from app.config import settings

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer

log = logging.getLogger(__name__)

_INSTANCE: "EmbeddingService | None" = None
_LOCK = threading.Lock()


class EmbeddingService:
    """Thread-safe singleton wrapper around a SentenceTransformer model."""

    def __init__(self, model_name: str = settings.EMBED_MODEL, device: str = settings.EMBED_DEVICE) -> None:
        self._model_name = model_name
        self._device = device
        self._model: "SentenceTransformer | None" = None
        self._model_lock = threading.Lock()

    # ── Public API ────────────────────────────────────────────────────────

    @property
    def dim(self) -> int:
        """Output vector dimensionality (loads model if not yet loaded)."""
        return int(self._get_model().get_sentence_embedding_dimension())

    def encode(self, texts: list[str] | str) -> np.ndarray:
        """
        Encode one or more texts into L2-normalised embedding vectors.

        Args:
            texts: A single string or a list of strings.

        Returns:
            ``np.ndarray`` of shape ``(len(texts), dim)`` with dtype ``float32``.
            For a single string input, shape is ``(1, dim)``.
        """
        if isinstance(texts, str):
            texts = [texts]
        if not texts:
            return np.empty((0, self.dim), dtype=np.float32)

        texts = [t.strip() or " " for t in texts]
        model = self._get_model()
        vectors: np.ndarray = model.encode(
            texts,
            batch_size=settings.EMBED_BATCH_SIZE,
            normalize_embeddings=True,   # L2 normalise → cosine via dot product
            show_progress_bar=False,
            convert_to_numpy=True,
        )
        return vectors.astype(np.float32)

    def encode_query(self, text: str) -> np.ndarray:
        """Encode a single query string; returns shape ``(dim,)``."""
        return self.encode([text])[0]

    def warmup(self) -> None:
        """Trigger model load eagerly (e.g. during app startup lifespan)."""
        _ = self._get_model()
        log.info("EmbeddingService warmed up — model=%r  dim=%d", self._model_name, self.dim)

    # ── Internal ──────────────────────────────────────────────────────────

    def _get_model(self) -> "SentenceTransformer":
        if self._model is None:
            with self._model_lock:
                if self._model is None:
                    from sentence_transformers import SentenceTransformer  # local import keeps startup fast
                    log.info("Loading embedding model %r on device=%r …", self._model_name, self._device)
                    self._model = SentenceTransformer(self._model_name, device=self._device)
        return self._model


# ── Module-level singleton ────────────────────────────────────────────────────

def get_embedding_service() -> EmbeddingService:
    """Return the process-wide singleton EmbeddingService (created lazily)."""
    global _INSTANCE
    if _INSTANCE is None:
        with _LOCK:
            if _INSTANCE is None:
                _INSTANCE = EmbeddingService()
    return _INSTANCE
