from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Literal

from app.core.config import settings
from app.core.logging import get_logger
from app.embeddings.service import embed_batch
from app.vector_store.qdrant import Document, upsert_documents

log = get_logger(__name__)

Domain = Literal["career", "college", "scholarship", "exam", "faq", "roadmap", "general"]

CHUNK_SIZE = 512   # tokens approx (chars / 4)
CHUNK_OVERLAP = 64


@dataclass
class RawDocument:
    text: str
    domain: Domain
    source: str
    title: str
    metadata: dict = field(default_factory=dict)


def _split_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Sentence-aware chunking with overlap."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks, current, current_len = [], [], 0
    for sent in sentences:
        tokens = len(sent) // 4
        if current_len + tokens > chunk_size and current:
            chunks.append(" ".join(current))
            # overlap: keep last N sentences
            overlap_sents = []
            overlap_len = 0
            for s in reversed(current):
                overlap_len += len(s) // 4
                if overlap_len > overlap:
                    break
                overlap_sents.insert(0, s)
            current = overlap_sents
            current_len = sum(len(s) // 4 for s in current)
        current.append(sent)
        current_len += tokens
    if current:
        chunks.append(" ".join(current))
    return [c for c in chunks if len(c.strip()) > 50]


def _make_id(source: str, chunk_idx: int) -> str:
    h = hashlib.sha256(f"{source}::{chunk_idx}".encode()).hexdigest()[:16]
    return h


def _domain_to_collection(domain: Domain) -> str:
    return {
        "career": settings.COLLECTION_CAREERS,
        "college": settings.COLLECTION_COLLEGES,
        "scholarship": settings.COLLECTION_SCHOLARSHIPS,
        "exam": settings.COLLECTION_EXAMS,
        "faq": settings.COLLECTION_FAQS,
        "roadmap": settings.COLLECTION_ROADMAPS,
        "general": settings.COLLECTION_CAREERS,
    }.get(domain, settings.COLLECTION_CAREERS)


def ingest_documents(raw_docs: list[RawDocument], batch_size: int = 32) -> dict:
    total_chunks = 0
    for raw in raw_docs:
        collection = _domain_to_collection(raw.domain)
        chunks = _split_text(raw.text)
        if not chunks:
            continue

        # Process in batches
        for i in range(0, len(chunks), batch_size):
            batch_chunks = chunks[i:i + batch_size]
            embed_results = embed_batch(batch_chunks)
            docs = []
            for j, (chunk, embed) in enumerate(zip(batch_chunks, embed_results)):
                doc_id = _make_id(raw.source, i + j)
                docs.append(Document(
                    id=doc_id,
                    text=chunk,
                    metadata={
                        "domain": raw.domain,
                        "source": raw.source,
                        "title": raw.title,
                        "chunk_idx": i + j,
                        **raw.metadata,
                    },
                    dense=embed.dense,
                    sparse=embed.sparse,
                ))
            upsert_documents(collection, docs)
            total_chunks += len(docs)
            log.info("Ingested chunks %d-%d for '%s'", i, i + len(batch_chunks), raw.source)

    return {"status": "ok", "total_chunks": total_chunks, "documents": len(raw_docs)}
