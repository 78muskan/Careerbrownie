from __future__ import annotations

from app.core.config import settings
from app.core.logging import get_logger
from app.embeddings.service import embed_text
from app.vector_store.qdrant import SearchResult, hybrid_search

log = get_logger(__name__)


def retrieve(
    query: str,
    collections: list[str] | None = None,
    top_k: int | None = None,
    filter_: dict | None = None,
) -> list[SearchResult]:
    """Hybrid retrieval across one or more Qdrant collections."""
    if collections is None:
        collections = [
            settings.COLLECTION_CAREERS,
            settings.COLLECTION_COLLEGES,
            settings.COLLECTION_SCHOLARSHIPS,
            settings.COLLECTION_EXAMS,
            settings.COLLECTION_FAQS,
        ]
    k = top_k or settings.RAG_RETRIEVE_TOP_K
    try:
        embed = embed_text(query)
    except Exception as exc:
        log.warning("embed_text failed, skipping retrieval: %s", exc)
        return []

    all_results: list[SearchResult] = []
    per_collection = max(1, k // len(collections))

    for col in collections:
        try:
            results = hybrid_search(
                collection=col,
                dense=embed.dense,
                sparse=embed.sparse,
                top_k=per_collection,
                filter_=filter_,
            )
            all_results.extend(results)
        except Exception as exc:
            log.warning("Retrieval failed for collection %s: %s", col, exc)

    # Deduplicate by id, keep highest score
    seen: dict[str, SearchResult] = {}
    for r in all_results:
        if r.id not in seen or r.score > seen[r.id].score:
            seen[r.id] = r

    return sorted(seen.values(), key=lambda x: x.score, reverse=True)[:k]
