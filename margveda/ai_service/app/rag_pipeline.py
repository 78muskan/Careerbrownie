"""RAG pipeline — the central orchestrator of the AI service.

End-to-end request flow
------------------------
::

    RAGPipeline.process(query, domain, history, profile)
        ├── 1. RAGCache.get(key)                         → cached response (fast path)
        ├── 2. Retriever.retrieve(query, domain)         → RetrievalResult list
        ├── 3. PromptBuilder.build(...)                  → PromptPackage (numbered [1][2] context)
        ├── 4. LLMClient.chat(messages, system)          → LLMResponse (Ollama → Claude → fallback)
        ├── 5. build_citations(retrieved)                → Citation list
        ├── 6. PromptBuilder.extract_suggestions(text)  → SuggestedAction list
        ├── 7. RAGCache.set(key, response)               → cached for next request
        └── ────────────────────────────────────────────── RAGResponse

Example trace (query = "What is the cutoff for IIT Bombay CS?")
-----------------------------------------------------------------
- Query embedding computed: 384-dim vector
- Top-6 chunks retrieved from ChromaDB: IIT Bombay profile (0.88), JEE Advanced (0.82), ...
- Prompt built: [1] IIT Bombay (college) ... [2] JEE Advanced (exam) ...
- Ollama generates: "IIT Bombay CS requires a JEE Advanced rank below 67 [1]..."
- Citations: [{index:1, title:"IIT Bombay", domain:"college", score:0.88}, ...]
- Response cached under SHA-256 key; returned with latency_ms
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

from app.cache import RAGCache
from app.config import settings
from app.embedding_service import EmbeddingService, get_embedding_service
from app.llm_client import LLMClient, LLMResponse
from app.prompt_builder import (
    Message, PromptBuilder, SuggestedAction, build_fallback_response,
    needs_counselor_escalation,
)
from app.retriever import Retriever, RetrievalResult
from app.chroma_store import VectorStore

log = logging.getLogger(__name__)


# ── Public data types ─────────────────────────────────────────────────────────

@dataclass
class Citation:
    """One source cited in the answer, corresponding to a numbered [N] reference."""
    index: int         # position in the answer: [1], [2], …
    id: str            # chunk id in the vector store
    title: str         # human-readable title from metadata
    domain: str        # career | college | exam | scholarship | …
    score: float       # cosine similarity score from retrieval


@dataclass
class RAGResponse:
    answer: str
    sources: list[str]                   # chunk ids used for grounding
    citations: list[Citation] = field(default_factory=list)
    suggestions: list[SuggestedAction] = field(default_factory=list)
    latency_ms: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    from_fallback: bool = False
    from_cache: bool = False
    needs_counselor: bool = False        # True → frontend shows "Book a session" CTA
    counselor_reason: str = ""


# ── RAGPipeline ───────────────────────────────────────────────────────────────

class RAGPipeline:
    """
    Orchestrates retrieval, prompt construction, LLM generation, and caching
    for one conversation turn.

    The pipeline is stateless per call; session history is passed in and
    updated by the caller.  This makes it safe for concurrent requests.

    Args:
        vector_store: Initialised :class:`VectorStore`.
        llm_client: Initialised :class:`LLMClient`.
        embedding_service: Initialised :class:`EmbeddingService`.
        cache: Initialised :class:`RAGCache` (or ``None`` to disable caching).
        top_k: Number of chunks to retrieve.
        min_score: Minimum cosine similarity threshold.
    """

    def __init__(
        self,
        vector_store: VectorStore,
        llm_client: LLMClient,
        embedding_service: EmbeddingService | None = None,
        cache: RAGCache | None = None,
        top_k: int = settings.RETRIEVAL_TOP_K,
        min_score: float = settings.RETRIEVAL_MIN_SCORE,
    ) -> None:
        embed = embedding_service or get_embedding_service()
        self._retriever = Retriever(vector_store, embed, top_k=top_k, min_score=min_score)
        self._prompt_builder = PromptBuilder(max_context_chars=settings.MAX_CONTEXT_CHARS)
        self._llm = llm_client
        self._cache = cache or RAGCache()

    # ── Public API ────────────────────────────────────────────────────────────

    async def process(
        self,
        query: str,
        history: list[Message] | None = None,
        student_profile: dict | None = None,
        *,
        domain: str | None = None,
    ) -> RAGResponse:
        """
        Process one user query and return a grounded, cited answer.

        Args:
            query: The user's raw question text.
            history: Previous turns (oldest first). Mutate after the call.
            student_profile: Optional context: stream, class_level, interests, goal.
            domain: Restrict retrieval to a specific knowledge domain
                    (``"career"``, ``"college"``, ``"exam"``, ``"faq"``, etc.)

        Returns:
            :class:`RAGResponse` with the answer, citations, and metadata.
        """
        t0 = time.monotonic()
        query = query.strip()
        if not query:
            return RAGResponse(answer="Please type a question and I'll be happy to help!", sources=[])

        # ── 1. Cache check ────────────────────────────────────────────────────
        cache_key = self._cache.make_key(query, domain=domain, profile=student_profile)
        cached = self._cache.get(cache_key)
        if cached:
            log.debug("Cache hit for query=%r", query[:60])
            return _response_from_dict(cached, from_cache=True)

        # ── 2. Retrieve relevant chunks ───────────────────────────────────────
        retrieved: list[RetrievalResult] = self._retriever.retrieve(query, domain=domain)
        log.debug("Retrieved %d chunks for query=%r", len(retrieved), query[:60])

        # ── 3. Build prompt (numbered [1][2] citations in context) ────────────
        package = self._prompt_builder.build(
            query=query,
            retrieved=retrieved,
            history=history,
            student_profile=student_profile,
        )

        # ── 4. Generate answer via LLM ────────────────────────────────────────
        fallback_text = build_fallback_response(query, retrieved)
        llm_resp: LLMResponse = await self._llm.chat(
            messages=package.messages,
            system=package.system,
            fallback_text=fallback_text,
        )

        # ── 5. Build citation objects ─────────────────────────────────────────
        citations = _build_citations(retrieved)

        # ── 6. Extract follow-up suggestions ──────────────────────────────────
        suggestions = self._prompt_builder.extract_suggestions(llm_resp.text)

        # ── 7. Counselor escalation detection ─────────────────────────────────
        min_score = min((r.score for r in retrieved), default=0.0)
        flag_counselor = needs_counselor_escalation(query, llm_resp.text, min_score)
        counselor_reason = ""
        if flag_counselor:
            counselor_reason = (
                "This question involves personal circumstances that benefit from "
                "one-on-one expert guidance."
            )

        latency_ms = int((time.monotonic() - t0) * 1000)
        log.info(
            "RAG: latency=%dms  tokens=%d+%d  sources=%d  fallback=%s  model=%s  counselor=%s",
            latency_ms, llm_resp.input_tokens, llm_resp.output_tokens,
            len(retrieved), llm_resp.from_fallback, llm_resp.model, flag_counselor,
        )

        response = RAGResponse(
            answer=llm_resp.text,
            sources=package.context_used,
            citations=citations,
            suggestions=suggestions,
            latency_ms=latency_ms,
            input_tokens=llm_resp.input_tokens,
            output_tokens=llm_resp.output_tokens,
            from_fallback=llm_resp.from_fallback,
            from_cache=False,
            needs_counselor=flag_counselor,
            counselor_reason=counselor_reason,
        )

        # ── 7. Cache successful non-fallback responses ────────────────────────
        if not llm_resp.from_fallback:
            self._cache.set(cache_key, _response_to_dict(response))

        return response

    async def ingest_chunks(
        self,
        texts: list[str],
        ids: list[str],
        metadatas: list[dict],
    ) -> int:
        """
        Encode and store pre-chunked texts into the vector store.

        Called by the document ingestion flow in main.py.

        Returns the number of chunks stored.
        """
        if not texts:
            return 0
        embed = get_embedding_service()
        vectors = embed.encode(texts)
        n = self._retriever._store.upsert(
            ids=ids,
            embeddings=vectors,
            texts=texts,
            metadatas=metadatas,
        )
        log.info("Ingested %d chunks into vector store", n)
        return n


# ── Helpers ───────────────────────────────────────────────────────────────────

def _build_citations(retrieved: list[RetrievalResult]) -> list[Citation]:
    """Convert retrieval results to Citation objects numbered [1][2]…"""
    return [
        Citation(
            index=i,
            id=r.id,
            title=r.metadata.get("title", r.id),
            domain=r.metadata.get("domain", ""),
            score=round(r.score, 4),
        )
        for i, r in enumerate(retrieved, start=1)
    ]


def _response_to_dict(r: RAGResponse) -> dict:
    return {
        "answer": r.answer,
        "sources": r.sources,
        "citations": [
            {"index": c.index, "id": c.id, "title": c.title, "domain": c.domain, "score": c.score}
            for c in r.citations
        ],
        "suggestions": [
            {"label": s.label, "value": s.value, "type": s.type} for s in r.suggestions
        ],
        "latency_ms": r.latency_ms,
        "input_tokens": r.input_tokens,
        "output_tokens": r.output_tokens,
        "from_fallback": r.from_fallback,
        "needs_counselor": r.needs_counselor,
        "counselor_reason": r.counselor_reason,
    }


def _response_from_dict(d: dict, *, from_cache: bool = True) -> RAGResponse:
    return RAGResponse(
        answer=d["answer"],
        sources=d.get("sources", []),
        citations=[
            Citation(index=c["index"], id=c["id"], title=c["title"], domain=c["domain"], score=c["score"])
            for c in d.get("citations", [])
        ],
        suggestions=[
            SuggestedAction(label=s["label"], value=s["value"], type=s.get("type", "query"))
            for s in d.get("suggestions", [])
        ],
        latency_ms=d.get("latency_ms", 0),
        input_tokens=d.get("input_tokens", 0),
        output_tokens=d.get("output_tokens", 0),
        from_fallback=d.get("from_fallback", False),
        from_cache=from_cache,
        needs_counselor=d.get("needs_counselor", False),
        counselor_reason=d.get("counselor_reason", ""),
    )
