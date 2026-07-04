"""Retriever — turns a query string into ranked document chunks.

Architecture::

    query (str)
        ↓  EmbeddingService.encode_query
    query_vector (ndarray)
        ↓  VectorStore.search
    raw_results (list[SearchResult])
        ↓  score filtering + optional domain filter
    RetrievalResult list  (returned to RAGPipeline)

Design decisions:
- Scores below ``settings.RETRIEVAL_MIN_SCORE`` are discarded so low-quality
  matches do not pollute the LLM context.
- The retriever does NOT re-rank; re-ranking is a future extension point.
- ``domain`` filter is optional — passing it restricts search to a specific
  knowledge partition (career, faq, college).
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

from app.config import settings
from app.embedding_service import EmbeddingService, get_embedding_service
from app.chroma_store import VectorStore, SearchResult

log = logging.getLogger(__name__)


# ── Public data types ─────────────────────────────────────────────────────────

@dataclass
class RetrievalResult:
    id: str
    text: str
    score: float
    metadata: dict
    rank: int


# ── Retriever ─────────────────────────────────────────────────────────────────

class Retriever:
    """
    Semantic retriever that converts a text query into embedding space and
    fetches the nearest neighbours from the vector store.

    Args:
        vector_store: Initialised :class:`VectorStore` instance.
        embedding_service: Initialised :class:`EmbeddingService` instance.
        top_k: Maximum candidates to fetch before score filtering.
        min_score: Minimum cosine similarity to keep a result.
    """

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_service: EmbeddingService | None = None,
        top_k: int = settings.RETRIEVAL_TOP_K,
        min_score: float = settings.RETRIEVAL_MIN_SCORE,
    ) -> None:
        self._store = vector_store
        self._embed = embedding_service or get_embedding_service()
        self._top_k = top_k
        self._min_score = min_score

    # ── Public API ────────────────────────────────────────────────────────

    def retrieve(
        self,
        query: str,
        *,
        top_k: int | None = None,
        min_score: float | None = None,
        domain: str | None = None,
    ) -> list[RetrievalResult]:
        """
        Find the most relevant document chunks for *query*.

        Args:
            query: Natural-language question or statement.
            top_k: Override the default top-k for this call.
            min_score: Override the minimum similarity threshold.
            domain: Optional metadata filter; e.g. ``"career"`` or ``"faq"``.

        Returns:
            List of :class:`RetrievalResult` sorted by descending score, with ranks
            starting at 1.  Empty list if the store has no matching content.
        """
        query = query.strip()
        if not query:
            return []

        k = top_k if top_k is not None else self._top_k
        min_s = min_score if min_score is not None else self._min_score

        # Encode query
        query_vec = self._embed.encode_query(query)

        # Build metadata filter for ChromaDB
        where = {"domain": domain} if domain else None

        raw: list[SearchResult] = self._store.search(
            query_embedding=query_vec,
            top_k=k,
            where=where,
        )

        # Filter below threshold
        filtered = [r for r in raw if r.score >= min_s]

        if not filtered:
            log.debug(
                "Retriever: no results above min_score=%.2f for query=%r  (domain=%s, raw=%d)",
                min_s,
                query[:60],
                domain,
                len(raw),
            )

        return [
            RetrievalResult(
                id=r.id,
                text=r.text,
                score=r.score,
                metadata=r.metadata,
                rank=i + 1,
            )
            for i, r in enumerate(filtered)
        ]

    def retrieve_multi_query(
        self,
        queries: list[str],
        *,
        top_k: int | None = None,
        min_score: float | None = None,
        domain: str | None = None,
    ) -> list[RetrievalResult]:
        """
        Retrieve for multiple query variants and return a deduplicated, re-ranked list.

        Useful when the RAG pipeline rewrites the user query into N variants to
        improve recall.  Deduplication is by chunk id; the highest score wins.
        """
        seen: dict[str, RetrievalResult] = {}
        for q in queries:
            for result in self.retrieve(q, top_k=top_k, min_score=min_score, domain=domain):
                existing = seen.get(result.id)
                if existing is None or result.score > existing.score:
                    seen[result.id] = result

        merged = sorted(seen.values(), key=lambda r: r.score, reverse=True)
        k = top_k if top_k is not None else self._top_k
        merged = merged[:k]

        # Re-assign ranks after merge
        for i, r in enumerate(merged):
            r.rank = i + 1

        return merged
