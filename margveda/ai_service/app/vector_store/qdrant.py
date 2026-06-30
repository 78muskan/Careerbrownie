from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from app.core.config import settings
from app.core.logging import get_logger

log = get_logger(__name__)

_client = None


def get_client():
    global _client
    if _client is None:
        from qdrant_client import QdrantClient
        kwargs = {"url": settings.QDRANT_URL}
        if settings.QDRANT_API_KEY:
            kwargs["api_key"] = settings.QDRANT_API_KEY
        _client = QdrantClient(**kwargs)
        log.info("Qdrant client connected: %s", settings.QDRANT_URL)
    return _client


@dataclass
class Document:
    id: str
    text: str
    metadata: dict = field(default_factory=dict)
    dense: list[float] = field(default_factory=list)
    sparse: Optional[dict[int, float]] = None


@dataclass
class SearchResult:
    id: str
    text: str
    score: float
    metadata: dict = field(default_factory=dict)


def ensure_collection(name: str) -> None:
    from qdrant_client.models import (
        Distance, VectorParams, SparseVectorParams,
        SparseIndexParams, HnswConfigDiff,
    )
    client = get_client()
    existing = {c.name for c in client.get_collections().collections}
    if name in existing:
        return
    client.create_collection(
        collection_name=name,
        vectors_config={"dense": VectorParams(size=settings.QDRANT_DENSE_DIM, distance=Distance.COSINE)},
        sparse_vectors_config={"sparse": SparseVectorParams(index=SparseIndexParams(on_disk=False))},
        hnsw_config=HnswConfigDiff(m=16, ef_construct=100),
    )
    log.info("Created Qdrant collection: %s", name)


def upsert_documents(collection: str, docs: list[Document]) -> None:
    from qdrant_client.models import PointStruct, SparseVector
    client = get_client()
    ensure_collection(collection)
    points = []
    for doc in docs:
        vectors: dict = {"dense": doc.dense}
        if doc.sparse:
            indices = list(doc.sparse.keys())
            values = [doc.sparse[i] for i in indices]
            vectors["sparse"] = SparseVector(indices=indices, values=values)
        points.append(PointStruct(
            id=doc.id,
            vector=vectors,
            payload={"text": doc.text, **doc.metadata},
        ))
    client.upsert(collection_name=collection, points=points)
    log.debug("Upserted %d docs to %s", len(docs), collection)


def search_dense(
    collection: str,
    vector: list[float],
    top_k: int = 10,
    filter_: dict | None = None,
) -> list[SearchResult]:
    from qdrant_client.models import Filter, FieldCondition, MatchValue
    client = get_client()
    qfilter = None
    if filter_:
        conditions = [FieldCondition(key=k, match=MatchValue(value=v)) for k, v in filter_.items()]
        qfilter = Filter(must=conditions)
    hits = client.search(
        collection_name=collection,
        query_vector=("dense", vector),
        limit=top_k,
        query_filter=qfilter,
        with_payload=True,
    )
    return [
        SearchResult(
            id=str(h.id),
            text=h.payload.get("text", ""),
            score=h.score,
            metadata={k: v for k, v in h.payload.items() if k != "text"},
        )
        for h in hits
    ]


def search_sparse(
    collection: str,
    sparse: dict[int, float],
    top_k: int = 10,
    filter_: dict | None = None,
) -> list[SearchResult]:
    from qdrant_client.models import SparseVector, NamedSparseVector, Filter, FieldCondition, MatchValue
    client = get_client()
    qfilter = None
    if filter_:
        conditions = [FieldCondition(key=k, match=MatchValue(value=v)) for k, v in filter_.items()]
        qfilter = Filter(must=conditions)
    indices = list(sparse.keys())
    values = [sparse[i] for i in indices]
    hits = client.search(
        collection_name=collection,
        query_vector=NamedSparseVector(name="sparse", vector=SparseVector(indices=indices, values=values)),
        limit=top_k,
        query_filter=qfilter,
        with_payload=True,
    )
    return [
        SearchResult(
            id=str(h.id),
            text=h.payload.get("text", ""),
            score=h.score,
            metadata={k: v for k, v in h.payload.items() if k != "text"},
        )
        for h in hits
    ]


def hybrid_search(
    collection: str,
    dense: list[float],
    sparse: dict[int, float] | None,
    top_k: int = 10,
    filter_: dict | None = None,
    dense_weight: float | None = None,
    sparse_weight: float | None = None,
) -> list[SearchResult]:
    """RRF fusion of dense + sparse results."""
    dw = dense_weight if dense_weight is not None else settings.RAG_DENSE_WEIGHT
    sw = sparse_weight if sparse_weight is not None else settings.RAG_SPARSE_WEIGHT

    dense_results = search_dense(collection, dense, top_k=top_k * 2, filter_=filter_)

    if sparse is None or not sparse:
        return dense_results[:top_k]

    sparse_results = search_sparse(collection, sparse, top_k=top_k * 2, filter_=filter_)

    # Reciprocal Rank Fusion
    scores: dict[str, float] = {}
    payload_map: dict[str, SearchResult] = {}
    K = 60

    for rank, r in enumerate(dense_results):
        scores[r.id] = scores.get(r.id, 0.0) + dw / (K + rank + 1)
        payload_map[r.id] = r

    for rank, r in enumerate(sparse_results):
        scores[r.id] = scores.get(r.id, 0.0) + sw / (K + rank + 1)
        if r.id not in payload_map:
            payload_map[r.id] = r

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    return [SearchResult(id=rid, text=payload_map[rid].text, score=sc, metadata=payload_map[rid].metadata)
            for rid, sc in ranked]


def delete_document(collection: str, doc_id: str) -> None:
    get_client().delete(collection_name=collection, points_selector=[doc_id])


def collection_count(collection: str) -> int:
    try:
        return get_client().count(collection_name=collection).count
    except Exception:
        return 0
