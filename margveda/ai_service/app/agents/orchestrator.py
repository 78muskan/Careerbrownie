from __future__ import annotations

import re
from app.agents.base import AgentContext, AgentResult
from app.agents.career import CareerAgent
from app.agents.college import CollegeAgent
from app.agents.scholarship import ScholarshipAgent
from app.core.logging import get_logger
from app.memory.conversation import ConversationMemory
from app.rag.pipeline import RAGResult, run_rag
from app.llm.base import Message

log = get_logger(__name__)

_CAREER_PATTERNS = re.compile(r"\b(career|job|profession|role|field|domain|engineer|doctor|lawyer|design)\b", re.I)
_COLLEGE_PATTERNS = re.compile(r"\b(college|university|iit|nit|bits|iim|aiims|nlsiu|admission|cutoff|rank|seat)\b", re.I)
_SCHOLARSHIP_PATTERNS = re.compile(r"\b(scholarship|scholarship|stipend|funding|financial aid|nsp|pm|modi|sc |st |obc)\b", re.I)


def _detect_intent(query: str) -> list[str]:
    intents = []
    if _CAREER_PATTERNS.search(query):
        intents.append("career")
    if _COLLEGE_PATTERNS.search(query):
        intents.append("college")
    if _SCHOLARSHIP_PATTERNS.search(query):
        intents.append("scholarship")
    return intents or ["general"]


AGENT_REGISTRY = {
    "career": CareerAgent(),
    "college": CollegeAgent(),
    "scholarship": ScholarshipAgent(),
}


async def process_chat(
    message: str,
    session_id: str,
    student_profile: dict | None = None,
) -> dict:
    # ── Memory (best-effort — Redis may not be available) ────────────────────
    memory = ConversationMemory(session_id)
    history: list[Message] = []
    profile: dict = dict(student_profile or {})
    try:
        history_turns = await memory.get_history(last_n=10)
        history = [Message(role=t.role, content=t.content) for t in history_turns]
        stored_profile = await memory.get_profile()
        profile = {**stored_profile, **profile}
        if profile:
            await memory.set_profile(profile)
    except Exception as exc:
        log.warning("Redis unavailable, running without conversation memory: %s", exc)

    intents = _detect_intent(message)
    log.info("session=%s intents=%s", session_id, intents)

    # ── RAG (best-effort — Qdrant / embeddings may not be available) ─────────
    try:
        rag_result: RAGResult = await run_rag(
            query=message,
            history=history,
            student_profile=profile,
        )
    except Exception as exc:
        log.warning("RAG pipeline failed, falling back to plain LLM: %s", exc)
        from app.llm.ollama import get_llm
        from app.llm.prompts import CAREER_COUNSELLOR_SYSTEM
        try:
            llm = await get_llm()
            msgs = [
                Message(role="system", content=CAREER_COUNSELLOR_SYSTEM),
                *history[-6:],
                Message(role="user", content=message),
            ]
            llm_resp = await llm.chat(msgs)
            rag_result = RAGResult(
                reply=llm_resp.content,
                suggested_actions=["Get career recommendations", "Take assessment", "Book consultation"],
                model=llm_resp.model,
            )
        except Exception as llm_exc:
            log.error("LLM also failed: %s", llm_exc)
            rag_result = RAGResult(
                reply=(
                    "I'm having trouble connecting to the AI right now. "
                    "Please try again in a moment or book a consultation with our human experts."
                ),
                suggested_actions=["Book consultation", "Try again"],
            )

    # ── Specialist agents (best-effort) ──────────────────────────────────────
    agent_data: dict[str, dict] = {}
    if intents != ["general"]:
        ctx = AgentContext(
            session_id=session_id,
            user_query=message,
            student_profile=profile,
            history=history,
        )
        for intent in intents:
            if intent in AGENT_REGISTRY:
                try:
                    result: AgentResult = await AGENT_REGISTRY[intent].run(ctx)
                    if result.confidence > 0.5:
                        agent_data[intent] = result.data
                except Exception as exc:
                    log.warning("Agent %s failed: %s", intent, exc)

    # ── Persist turn (best-effort) ───────────────────────────────────────────
    try:
        await memory.append("user", message)
        await memory.append("assistant", rag_result.reply)
    except Exception:
        pass

    return {
        "reply": rag_result.reply,
        "suggested_actions": rag_result.suggested_actions,
        "sources": rag_result.sources,
        "agent_data": agent_data,
        "model": rag_result.model,
        "retrieved_docs": rag_result.retrieved_docs,
        "session_id": session_id,
    }
