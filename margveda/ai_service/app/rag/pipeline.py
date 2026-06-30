from __future__ import annotations

import json
from dataclasses import dataclass, field

from app.core.config import settings
from app.core.logging import get_logger
from app.embeddings.service import rerank
from app.llm.base import Message
from app.llm.ollama import get_llm
from app.llm.prompts import CAREER_COUNSELLOR_SYSTEM, RAG_CONTEXT_TEMPLATE, QUERY_REWRITE_SYSTEM
from app.rag.retrieval import retrieve
from app.vector_store.qdrant import SearchResult

log = get_logger(__name__)


@dataclass
class RAGResult:
    reply: str
    sources: list[dict] = field(default_factory=list)
    suggested_actions: list[str] = field(default_factory=list)
    retrieved_docs: int = 0
    model: str = ""
    latency_ms: float = 0.0


async def _rewrite_query(query: str, history: list[Message]) -> list[str]:
    """Expand query into multiple search queries for better recall."""
    try:
        llm = await get_llm()
        context = "\n".join(f"{m.role}: {m.content}" for m in history[-4:]) if history else ""
        prompt = f"Conversation context:\n{context}\n\nCurrent query: {query}" if context else query
        resp = await llm.chat(
            [Message(role="system", content=QUERY_REWRITE_SYSTEM),
             Message(role="user", content=prompt)],
            temperature=0.1,
            max_tokens=200,
        )
        parsed = json.loads(resp.content)
        return parsed.get("queries", [query])[:3]
    except Exception:
        return [query]


def _build_context(docs: list[SearchResult]) -> str:
    parts = []
    for i, doc in enumerate(docs, 1):
        title = doc.metadata.get("title", "Unknown")
        domain = doc.metadata.get("domain", "")
        source = doc.metadata.get("source", "")
        parts.append(f"[{i}] ({domain.upper()} | {title} | {source})\n{doc.text}")
    return "\n\n".join(parts)


def _extract_actions(text: str) -> tuple[str, list[str]]:
    if "ACTIONS:" not in text:
        return text.strip(), ["Get career recommendations", "Take assessment", "Book consultation"]
    parts = text.rsplit("ACTIONS:", 1)
    reply = parts[0].strip()
    try:
        actions = json.loads(parts[1].strip())
        if isinstance(actions, list):
            return reply, [str(a) for a in actions[:5]]
    except Exception:
        pass
    return reply, ["Get career recommendations", "Take assessment", "Book consultation"]


async def run_rag(
    query: str,
    history: list[Message] | None = None,
    collections: list[str] | None = None,
    student_profile: dict | None = None,
    use_query_rewrite: bool = True,
) -> RAGResult:
    import time
    t0 = time.monotonic()
    history = history or []

    # 1. Query rewriting for better recall
    if use_query_rewrite and len(query) > 10:
        queries = await _rewrite_query(query, history)
    else:
        queries = [query]

    # 2. Retrieve from each rewritten query and merge
    all_docs: dict[str, SearchResult] = {}
    for q in queries:
        docs = retrieve(q, collections=collections, top_k=settings.RAG_RETRIEVE_TOP_K)
        for d in docs:
            if d.id not in all_docs or d.score > all_docs[d.id].score:
                all_docs[d.id] = d

    candidate_docs = list(all_docs.values())

    # 3. Rerank
    if candidate_docs:
        passages = [d.text for d in candidate_docs]
        ranked = rerank(query, passages, top_k=settings.RAG_RERANK_TOP_K)
        top_docs = [candidate_docs[idx] for idx, _ in ranked]
    else:
        top_docs = []

    # 4. Build context-injected prompt
    messages = [Message(role="system", content=CAREER_COUNSELLOR_SYSTEM)]
    messages.extend(history[-settings.MEMORY_MAX_TURNS:])

    if top_docs:
        context_block = _build_context(top_docs)
        rag_injection = RAG_CONTEXT_TEMPLATE.format(context=context_block)
        user_content = f"{rag_injection}\n\nStudent question: {query}"
    else:
        user_content = query

    if student_profile:
        profile_summary = (
            f"\nStudent profile: Stream={student_profile.get('stream', 'Unknown')}, "
            f"Marks={student_profile.get('marks', 'Unknown')}, "
            f"Location={student_profile.get('location', 'Unknown')}, "
            f"Budget={student_profile.get('budget', 'Unknown')}, "
            f"Interests={','.join(student_profile.get('interests', []))}"
        )
        user_content = profile_summary + "\n\n" + user_content

    messages.append(Message(role="user", content=user_content))

    # 5. Generate
    llm = await get_llm()
    llm_resp = await llm.chat(messages)
    reply, actions = _extract_actions(llm_resp.content)

    sources = [
        {"title": d.metadata.get("title", ""), "source": d.metadata.get("source", ""), "domain": d.metadata.get("domain", ""), "score": round(d.score, 3)}
        for d in top_docs
    ]

    return RAGResult(
        reply=reply,
        sources=sources,
        suggested_actions=actions,
        retrieved_docs=len(top_docs),
        model=llm_resp.model,
        latency_ms=(time.monotonic() - t0) * 1000,
    )
