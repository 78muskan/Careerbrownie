from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Optional

import numpy as np

from app.core.config import settings
from app.core.logging import get_logger

log = get_logger(__name__)

_lock = threading.Lock()
_embed_model = None
_reranker_model = None


def _load_embed_model():
    global _embed_model
    if _embed_model is not None:
        return _embed_model
    with _lock:
        if _embed_model is not None:
            return _embed_model
        log.info("Loading embedding model: %s", settings.EMBED_MODEL)
        try:
            from FlagEmbedding import BGEM3FlagModel
            _embed_model = BGEM3FlagModel(
                settings.EMBED_MODEL,
                use_fp16=(settings.EMBED_DEVICE == "cuda"),
                device=settings.EMBED_DEVICE,
            )
            log.info("BGEM3FlagModel loaded (dense+sparse+colbert)")
        except ImportError:
            from sentence_transformers import SentenceTransformer
            _embed_model = SentenceTransformer(settings.EMBED_MODEL, device=settings.EMBED_DEVICE)
            log.warning("FlagEmbedding not found — using SentenceTransformer (dense only)")
    return _embed_model


def _load_reranker():
    global _reranker_model
    if _reranker_model is not None:
        return _reranker_model
    with _lock:
        if _reranker_model is not None:
            return _reranker_model
        log.info("Loading reranker: %s", settings.RERANKER_MODEL)
        try:
            from FlagEmbedding import FlagReranker
            _reranker_model = FlagReranker(settings.RERANKER_MODEL, use_fp16=(settings.EMBED_DEVICE == "cuda"))
        except ImportError:
            log.warning("FlagEmbedding not available — reranking disabled")
            _reranker_model = None
    return _reranker_model


@dataclass
class EmbedResult:
    dense: list[float]
    sparse: Optional[dict[int, float]] = None  # token_id -> weight


def embed_text(text: str) -> EmbedResult:
    model = _load_embed_model()
    try:
        # FlagEmbedding path — returns dense, lexical_weights, colbert_vecs
        out = model.encode(
            [text],
            batch_size=1,
            max_length=settings.EMBED_MAX_LENGTH,
            return_dense=True,
            return_sparse=True,
            return_colbert_vecs=False,
        )
        dense = out["dense_vecs"][0].tolist()
        sparse_weights = out["lexical_weights"][0]
        # Convert to {int: float} dict
        sparse = {int(k): float(v) for k, v in sparse_weights.items() if float(v) > 0.0}
        return EmbedResult(dense=dense, sparse=sparse)
    except (AttributeError, TypeError):
        # SentenceTransformer fallback (dense only)
        dense = model.encode(text, normalize_embeddings=True).tolist()
        return EmbedResult(dense=dense, sparse=None)


def embed_batch(texts: list[str]) -> list[EmbedResult]:
    model = _load_embed_model()
    results = []
    try:
        out = model.encode(
            texts,
            batch_size=settings.EMBED_BATCH_SIZE,
            max_length=settings.EMBED_MAX_LENGTH,
            return_dense=True,
            return_sparse=True,
            return_colbert_vecs=False,
        )
        for i in range(len(texts)):
            dense = out["dense_vecs"][i].tolist()
            sparse_weights = out["lexical_weights"][i]
            sparse = {int(k): float(v) for k, v in sparse_weights.items() if float(v) > 0.0}
            results.append(EmbedResult(dense=dense, sparse=sparse))
    except (AttributeError, TypeError):
        vecs = model.encode(texts, batch_size=settings.EMBED_BATCH_SIZE, normalize_embeddings=True)
        for v in vecs:
            results.append(EmbedResult(dense=v.tolist(), sparse=None))
    return results


def rerank(query: str, passages: list[str], top_k: int | None = None) -> list[tuple[int, float]]:
    """Returns (original_index, score) sorted desc."""
    reranker = _load_reranker()
    if reranker is None or not passages:
        return [(i, 1.0 / (i + 1)) for i in range(len(passages))]
    pairs = [[query, p] for p in passages]
    scores = reranker.compute_score(pairs, normalize=True)
    if isinstance(scores, float):
        scores = [scores]
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    k = top_k or settings.RERANKER_TOP_K
    return [(idx, float(score)) for idx, score in ranked[:k]]
