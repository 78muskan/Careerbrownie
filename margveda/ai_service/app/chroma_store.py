"""ChromaDB-backed vector store.

Wraps ChromaDB's PersistentClient to provide a stable interface for the rest
of the AI service.  All embeddings are produced externally (by EmbeddingService)
and passed explicitly so ChromaDB never calls its own embedding function.

One collection per store instance; created or opened on first access.

Thread-safety: ChromaDB's PersistentClient is thread-safe for concurrent reads.
Writes are serialised via the collection's internal locking.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import chromadb
import numpy as np

from app.config import settings

log = logging.getLogger(__name__)

_DISTANCE_KEY = "distances"


# ── Public data types ─────────────────────────────────────────────────────────

@dataclass
class SearchResult:
    id: str
    text: str
    score: float          # cosine similarity [0, 1]
    metadata: dict


# ── VectorStore ───────────────────────────────────────────────────────────────

class VectorStore:
    """
    Persistent, file-based vector store using ChromaDB.

    Usage::

        store = VectorStore()
        store.upsert(ids=["a"], embeddings=np.array([[0.1, ...]]), texts=["hello"], metadatas=[{}])
        results = store.search(query_embedding=np.array([0.1, ...]), top_k=5)
    """

    def __init__(
        self,
        persist_dir: str = settings.CHROMA_PERSIST_DIR,
        collection_name: str = settings.COLLECTION_NAME,
    ) -> None:
        self._client = chromadb.PersistentClient(path=persist_dir)
        # cosine space: distance = 1 - similarity, so closer = smaller distance
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        log.info(
            "VectorStore ready — collection=%r  persist_dir=%r  count=%d",
            collection_name,
            persist_dir,
            self.count(),
        )

    # ── Write ─────────────────────────────────────────────────────────────

    def upsert(
        self,
        ids: list[str],
        embeddings: np.ndarray,
        texts: list[str],
        metadatas: list[dict] | None = None,
    ) -> int:
        """Insert or update documents.  Returns the number of items stored."""
        if not ids:
            return 0
        if len(ids) != len(texts) or len(ids) != embeddings.shape[0]:
            raise ValueError("ids, texts, and embeddings must have equal length")

        # ChromaDB accepts Python lists of float lists
        emb_list: list[list[float]] = embeddings.tolist()
        meta_list: list[dict] = (
            [_sanitise_metadata(m) for m in metadatas]
            if metadatas
            else [{} for _ in ids]
        )

        self._collection.upsert(
            ids=ids,
            embeddings=emb_list,
            documents=texts,
            metadatas=meta_list,
        )
        return len(ids)

    def delete(self, ids: list[str]) -> None:
        """Delete documents by id."""
        if ids:
            self._collection.delete(ids=ids)

    def delete_where(self, where: dict[str, Any]) -> None:
        """Delete all documents matching a ChromaDB where-filter, e.g. ``{"domain": "faq"}``."""
        self._collection.delete(where=where)

    # ── Read ──────────────────────────────────────────────────────────────

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = settings.RETRIEVAL_TOP_K,
        where: dict | None = None,
    ) -> list[SearchResult]:
        """Find the *top_k* most similar documents.

        Args:
            query_embedding: 1-D or 2-D float array (single query vector).
            top_k: Maximum number of results.
            where: Optional ChromaDB metadata filter, e.g. ``{"domain": "career"}``.

        Returns:
            List of :class:`SearchResult` sorted by descending similarity.
        """
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)

        n = min(top_k, self.count())
        if n == 0:
            return []

        kwargs: dict[str, Any] = dict(
            query_embeddings=query_embedding.tolist(),
            n_results=n,
            include=["documents", "metadatas", "distances"],
        )
        if where:
            kwargs["where"] = where

        raw = self._collection.query(**kwargs)
        results: list[SearchResult] = []

        ids_batch = raw.get("ids", [[]])[0]
        docs_batch = raw.get("documents", [[]])[0]
        metas_batch = raw.get("metadatas", [[]])[0]
        dists_batch = raw.get(_DISTANCE_KEY, [[]])[0]

        for doc_id, text, meta, dist in zip(ids_batch, docs_batch, metas_batch, dists_batch):
            # cosine distance ∈ [0, 2] → similarity ∈ [-1, 1] → clamp to [0, 1]
            score = max(0.0, min(1.0, 1.0 - float(dist)))
            results.append(
                SearchResult(id=str(doc_id), text=str(text), score=score, metadata=dict(meta))
            )

        return sorted(results, key=lambda r: r.score, reverse=True)

    def count(self) -> int:
        """Return total number of documents in the collection."""
        return self._collection.count()

    def collection_name(self) -> str:
        return self._collection.name


# ── Helpers ───────────────────────────────────────────────────────────────────

def _sanitise_metadata(meta: dict) -> dict:
    """ChromaDB only accepts str, int, float, or bool values."""
    sanitised: dict = {}
    for k, v in meta.items():
        if isinstance(v, (str, int, float, bool)):
            sanitised[str(k)] = v
        elif v is None:
            sanitised[str(k)] = ""
        else:
            sanitised[str(k)] = str(v)
    return sanitised
