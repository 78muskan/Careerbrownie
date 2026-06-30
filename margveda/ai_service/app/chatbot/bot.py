"""
Backward-compatible chatbot interface.
Delegates to the full RAG + Agent pipeline (Qwen2.5 via Ollama).
Falls back to Anthropic API if Ollama is unavailable.
"""
from __future__ import annotations

import asyncio
import json
import uuid

from app.models.schemas import ChatMessageRequest, ChatMessageResponse


def chat(payload: ChatMessageRequest) -> ChatMessageResponse:
    """Sync wrapper used by legacy /chatbot/chat callers."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as pool:
            future = pool.submit(asyncio.run, _async_chat(payload))
            return future.result(timeout=90)
    return loop.run_until_complete(_async_chat(payload))


async def _async_chat(payload: ChatMessageRequest) -> ChatMessageResponse:
    from app.agents.orchestrator import process_chat

    session_id = (payload.student_context or {}).get("session_id") or str(uuid.uuid4())
    profile = None
    if payload.student_context:
        ctx = payload.student_context
        profile = {k: v for k, v in {
            "interests": ctx.get("interests", []),
            "skills": ctx.get("skills", []),
            "stream": ctx.get("stream", ""),
            "marks": ctx.get("marks", ""),
        }.items() if v}

    try:
        result = await process_chat(
            message=payload.message,
            session_id=session_id,
            student_profile=profile or None,
        )
        return ChatMessageResponse(
            reply=result["reply"],
            suggested_actions=result.get("suggested_actions", []),
        )
    except Exception:
        return await _anthropic_fallback(payload)


async def _anthropic_fallback(payload: ChatMessageRequest) -> ChatMessageResponse:
    import os, httpx
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return _rule_based(payload.message)

    SYSTEM = (
        "You are Career Brownie AI, an expert career counsellor for Indian students. "
        "Help with career planning, college admissions, skills, and scholarships. "
        "End every reply with: ACTIONS: [\"action1\", \"action2\", \"action3\"]"
    )
    history = []
    if payload.student_context:
        for entry in (payload.student_context.get("history") or [])[-10:]:
            if entry.get("role") in ("user", "assistant") and entry.get("content"):
                history.append({"role": entry["role"], "content": entry["content"]})
    history.append({"role": "user", "content": payload.message})
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={"x-api-key": api_key, "anthropic-version": "2023-06-01"},
                json={"model": "claude-sonnet-4-6", "max_tokens": 600, "system": SYSTEM, "messages": history},
            )
            r.raise_for_status()
        text = r.json()["content"][0]["text"].strip()
        reply, actions = text, ["Get career recommendations", "Take assessment", "Book consultation"]
        if "ACTIONS:" in text:
            parts = text.rsplit("ACTIONS:", 1)
            reply = parts[0].strip()
            try:
                actions = json.loads(parts[1].strip())
            except Exception:
                pass
        return ChatMessageResponse(reply=reply, suggested_actions=actions)
    except Exception:
        return _rule_based(payload.message)


def _rule_based(message: str) -> ChatMessageResponse:
    msg = message.lower()
    if any(w in msg for w in ("college", "iit", "nit", "admission", "cutoff")):
        return ChatMessageResponse(reply="Share your stream, score, and preferred states — I'll suggest the best colleges.", suggested_actions=["Try college predictor", "View cutoffs", "Book counsellor"])
    if any(w in msg for w in ("skill", "learn", "course", "gap")):
        return ChatMessageResponse(reply="Tell me your current skills and target career. I'll build a personalised learning plan.", suggested_actions=["Run skill gap analysis", "Generate roadmap", "Browse courses"])
    if any(w in msg for w in ("scholarship", "funding", "financial")):
        return ChatMessageResponse(reply="Share your category, income bracket, and marks. I'll find the best scholarships for you.", suggested_actions=["Find scholarships", "Check eligibility", "Apply now"])
    return ChatMessageResponse(
        reply="I'm Career Brownie AI. I help with career planning, college admissions, scholarships, and skill development. What would you like to explore?",
        suggested_actions=["Get career recommendations", "Take assessment", "Book consultation"],
    )
