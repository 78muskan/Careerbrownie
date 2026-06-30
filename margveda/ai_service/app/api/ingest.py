from __future__ import annotations

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Literal, Optional

from app.core.config import settings
from app.core.logging import get_logger
from app.rag.ingestion import RawDocument, ingest_documents
from app.vector_store.qdrant import collection_count

log = get_logger(__name__)
router = APIRouter(prefix="/ingest", tags=["ingest"])

_api_key_header = APIKeyHeader(name="X-Internal-Key", auto_error=False)


def _require_internal_key(key: str | None = Depends(_api_key_header)):
    if key != settings.INTERNAL_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid internal API key")


class IngestRequest(BaseModel):
    documents: list[dict]
    domain: Literal["career", "college", "scholarship", "exam", "faq", "roadmap", "general"]


class CollectionStats(BaseModel):
    careers: int
    colleges: int
    scholarships: int
    entrance_exams: int
    faqs: int
    roadmaps: int


@router.post("/", dependencies=[Depends(_require_internal_key)])
async def ingest(req: IngestRequest):
    raw_docs = [
        RawDocument(
            text=d.get("text", d.get("content", "")),
            domain=req.domain,
            source=d.get("source", "manual"),
            title=d.get("title", "Untitled"),
            metadata={k: v for k, v in d.items() if k not in ("text", "content", "source", "title")},
        )
        for d in req.documents
        if d.get("text") or d.get("content")
    ]
    if not raw_docs:
        raise HTTPException(status_code=400, detail="No valid documents provided")

    result = ingest_documents(raw_docs)
    return result


@router.get("/stats", dependencies=[Depends(_require_internal_key)], response_model=CollectionStats)
async def stats():
    return CollectionStats(
        careers=collection_count(settings.COLLECTION_CAREERS),
        colleges=collection_count(settings.COLLECTION_COLLEGES),
        scholarships=collection_count(settings.COLLECTION_SCHOLARSHIPS),
        entrance_exams=collection_count(settings.COLLECTION_EXAMS),
        faqs=collection_count(settings.COLLECTION_FAQS),
        roadmaps=collection_count(settings.COLLECTION_ROADMAPS),
    )
