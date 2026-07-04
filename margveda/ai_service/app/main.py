"""CareerBrownie AI Service — FastAPI entry point.

Startup sequence (lifespan)
----------------------------
1. EmbeddingService warm-up (loads sentence-transformers model into memory)
2. VectorStore initialisation (opens/creates ChromaDB persistent collection)
3. RAG cache initialisation (Redis if configured, in-memory LRU otherwise)
4. LLM client initialisation (Ollama → Claude → fallback)
5. RAG pipeline assembly
6. Knowledge seeding — if the collection is empty, all 9 knowledge domains are
   chunked, embedded, and stored (~92 documents × ~2 chunks each ≈ 185 vectors)

Routes
-------
POST  /chat                — main chat endpoint; returns answer + citations
POST  /ingest              — ingest custom documents (X-Internal-Key protected)
POST  /search              — raw similarity search without LLM (debug / frontend)
GET   /knowledge/domains   — list domain names and document counts
GET   /health              — liveness probe
GET   /stats               — collection + cache statistics
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.cache import RAGCache
from app.config import settings
from app.chunking import chunk_document
from app.document_loader import Document, load_from_dicts
from app.embedding_service import get_embedding_service
from app.llm_client import LLMClient
from app.prompt_builder import Message
from app.rag_pipeline import RAGPipeline
from app.chroma_store import VectorStore
from app.knowledge import get_all_documents, get_domain_stats

log = logging.getLogger(__name__)
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL, logging.INFO))

# ── Global service instances (initialised in lifespan) ───────────────────────

_pipeline: RAGPipeline | None = None
_vector_store: VectorStore | None = None
_llm_client: LLMClient | None = None
_cache: RAGCache | None = None


# ── Lifespan ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    global _pipeline, _vector_store, _llm_client, _cache

    log.info("=== CareerBrownie AI Service startup ===")

    # 1. Embedding model
    embed = get_embedding_service()
    embed.warmup()

    # 2. Vector store (ChromaDB persistent)
    _vector_store = VectorStore(
        persist_dir=settings.CHROMA_PERSIST_DIR,
        collection_name=settings.COLLECTION_NAME,
    )

    # 3. Cache (Redis or in-memory LRU)
    _cache = RAGCache()

    # 4. LLM client (Ollama primary → Claude fallback → rule-based)
    _llm_client = LLMClient()

    # 5. RAG pipeline
    _pipeline = RAGPipeline(
        vector_store=_vector_store,
        llm_client=_llm_client,
        embedding_service=embed,
        cache=_cache,
    )

    # 6. Seed all 9 knowledge domains if the collection is empty
    if _vector_store.count() == 0:
        log.info("Collection empty — seeding 9-domain knowledge base …")
        _seed_all_knowledge(embed)
        log.info("Seeding done: %d vectors in collection", _vector_store.count())
    else:
        log.info("Collection has %d vectors — skipping seed", _vector_store.count())

    log.info("=== Startup complete (LLM: %s) ===", _llm_client.model)
    yield

    if _llm_client:
        await _llm_client.close()
    log.info("AI service shut down")


def _seed_all_knowledge(embed: Any) -> None:
    """Chunk, embed, and store all 9 knowledge domains into ChromaDB."""
    assert _vector_store is not None

    all_raw = get_all_documents()   # ~92 domain records
    all_texts: list[str] = []
    all_ids: list[str] = []
    all_metas: list[dict] = []

    for raw in all_raw:
        base_meta = {
            "domain": raw.get("domain", "general"),
            "title": raw.get("title", ""),
            **(raw.get("metadata") or {}),
        }
        for chunk in chunk_document(
            text=raw["text"],
            doc_id=raw["id"],
            metadata=base_meta,
            chunk_size=settings.CHUNK_SIZE,
            overlap=settings.CHUNK_OVERLAP,
        ):
            all_texts.append(chunk.text)
            all_ids.append(chunk.id)
            all_metas.append(chunk.metadata)

    if all_texts:
        log.info("Encoding %d chunks across %d documents …", len(all_texts), len(all_raw))
        vectors = embed.encode(all_texts)
        _vector_store.upsert(ids=all_ids, embeddings=vectors, texts=all_texts, metadatas=all_metas)


# ── Application ───────────────────────────────────────────────────────────────

app = FastAPI(
    title="CareerBrownie AI Service",
    version=settings.VERSION,
    description="RAG-powered career guidance for Indian students — 9 knowledge domains, cited answers",
    docs_url="/docs" if not settings.is_production else None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ── Dependencies ──────────────────────────────────────────────────────────────

def get_pipeline() -> RAGPipeline:
    if _pipeline is None:
        raise HTTPException(status_code=503, detail="AI service not yet ready")
    return _pipeline


def require_internal_key(x_internal_key: str = Header(default="")) -> None:
    if x_internal_key != settings.INTERNAL_API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid X-Internal-Key")


# ── Schemas ───────────────────────────────────────────────────────────────────

class ConversationTurn(BaseModel):
    role: str = Field(pattern="^(user|assistant)$")
    content: str


class ChatRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)
    history: list[ConversationTurn] = Field(default_factory=list, max_length=20)
    student_profile: dict | None = None
    domain: str | None = Field(
        default=None,
        description="Restrict retrieval: career | college | exam | faq | scholarship | salary | skills | timeline | counsellor",
    )


class CitationOut(BaseModel):
    index: int
    id: str
    title: str
    domain: str
    score: float


class SuggestionOut(BaseModel):
    label: str
    value: str
    type: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    citations: list[CitationOut]
    suggestions: list[SuggestionOut]
    latency_ms: int
    from_fallback: bool
    from_cache: bool
    needs_counselor: bool = False
    counselor_reason: str = ""


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    domain: str | None = None
    top_k: int = Field(default=5, ge=1, le=20)


class SearchHit(BaseModel):
    id: str
    title: str
    domain: str
    score: float
    excerpt: str


class SearchResponse(BaseModel):
    query: str
    hits: list[SearchHit]
    total: int


class IngestRecord(BaseModel):
    text: str = Field(min_length=10)
    id: str | None = None
    title: str | None = None


class IngestRequest(BaseModel):
    documents: list[IngestRecord] = Field(min_length=1, max_length=200)
    domain: str = Field(default="general", max_length=40)


class IngestResponse(BaseModel):
    chunks_stored: int
    documents_processed: int


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    """Liveness probe — returns 200 when the service is ready."""
    count = _vector_store.count() if _vector_store else -1
    return {
        "status": "ok",
        "service": settings.SERVICE_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "llm_model": _llm_client.model if _llm_client else "none",
        "llm_available": _llm_client.is_available if _llm_client else False,
        "vector_store_vectors": count,
        "cache_size": _cache.size if _cache else 0,
    }


@app.get("/stats")
async def stats(pipeline: RAGPipeline = Depends(get_pipeline)):
    """Collection statistics and configuration overview."""
    store = pipeline._retriever._store
    return {
        "collection": store.collection_name(),
        "vector_count": store.count(),
        "domain_stats": get_domain_stats(),
        "embed_model": settings.EMBED_MODEL,
        "llm_model": _llm_client.model if _llm_client else "none",
        "retrieval_top_k": settings.RETRIEVAL_TOP_K,
        "retrieval_min_score": settings.RETRIEVAL_MIN_SCORE,
        "cache_size": _cache.size if _cache else 0,
        "cache_ttl_secs": settings.CACHE_TTL_SECS,
    }


@app.get("/knowledge/domains")
async def knowledge_domains():
    """
    List available knowledge domains with document counts.

    Returns::

        {
          "domains": {"career": 20, "college": 13, "exam": 13, ...},
          "total_documents": 92
        }
    """
    stats = get_domain_stats()
    return {
        "domains": stats,
        "total_documents": sum(stats.values()),
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    pipeline: RAGPipeline = Depends(get_pipeline),
):
    """
    Send a question; receive a grounded, cited answer from the knowledge base.

    The response includes:
    - ``answer``: Markdown-formatted text with inline [1][2] citation markers
    - ``citations``: List of sources cited, with title, domain, and similarity score
    - ``suggestions``: Up to 3 actionable follow-up queries
    - ``from_cache``: ``true`` when the response was served from cache (sub-millisecond)
    """
    history = [Message(role=t.role, content=t.content) for t in request.history]
    result = await pipeline.process(
        query=request.query,
        history=history,
        student_profile=request.student_profile,
        domain=request.domain,
    )
    return ChatResponse(
        answer=result.answer,
        sources=result.sources,
        citations=[
            CitationOut(index=c.index, id=c.id, title=c.title, domain=c.domain, score=c.score)
            for c in result.citations
        ],
        suggestions=[
            SuggestionOut(label=s.label, value=s.value, type=s.type)
            for s in result.suggestions
        ],
        latency_ms=result.latency_ms,
        from_fallback=result.from_fallback,
        from_cache=result.from_cache,
        needs_counselor=result.needs_counselor,
        counselor_reason=result.counselor_reason,
    )


@app.post("/search", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    pipeline: RAGPipeline = Depends(get_pipeline),
):
    """
    Raw similarity search — retrieves chunks without calling the LLM.

    Useful for:
    - Debugging retrieval quality before LLM generation
    - Frontend "related content" widgets
    - Checking whether a topic is covered in the knowledge base

    Does NOT consume LLM tokens.
    """
    from app.embedding_service import get_embedding_service as _get_emb
    embed = _get_emb()
    query_vec = embed.encode_query(request.query)
    store = pipeline._retriever._store
    domain_filter = {"domain": request.domain} if request.domain else None
    raw_hits = store.search(
        query_embedding=query_vec,
        top_k=request.top_k,
        where=domain_filter,
    )
    hits = [
        SearchHit(
            id=h.id,
            title=h.metadata.get("title", h.id),
            domain=h.metadata.get("domain", ""),
            score=round(h.score, 4),
            excerpt=h.text[:280].rstrip() + ("…" if len(h.text) > 280 else ""),
        )
        for h in raw_hits
    ]
    return SearchResponse(query=request.query, hits=hits, total=len(hits))


@app.post(
    "/ingest",
    response_model=IngestResponse,
    dependencies=[Depends(require_internal_key)],
)
async def ingest(
    request: IngestRequest,
    pipeline: RAGPipeline = Depends(get_pipeline),
):
    """
    Ingest custom documents into the vector store.

    Requires ``X-Internal-Key`` header matching ``INTERNAL_API_KEY`` in .env.
    Use this to add college-specific content, custom careers, or institution
    branding without modifying the built-in knowledge base.
    """
    embed = get_embedding_service()
    raw = [{"text": r.text, "id": r.id, "title": r.title} for r in request.documents]
    docs: list[Document] = load_from_dicts(raw, domain=request.domain)

    all_texts: list[str] = []
    all_ids: list[str] = []
    all_metas: list[dict] = []

    for doc in docs:
        for chunk in chunk_document(
            text=doc.text,
            doc_id=doc.id,
            metadata={**doc.metadata, "domain": request.domain},
            chunk_size=settings.CHUNK_SIZE,
            overlap=settings.CHUNK_OVERLAP,
        ):
            all_texts.append(chunk.text)
            all_ids.append(chunk.id)
            all_metas.append(chunk.metadata)

    stored = await pipeline.ingest_chunks(texts=all_texts, ids=all_ids, metadatas=all_metas)
    return IngestResponse(chunks_stored=stored, documents_processed=len(docs))
