from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel

from app.agents.orchestrator import process_chat
from app.core.config import settings
from app.core.logging import get_logger

log = get_logger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    student_profile: Optional[dict] = None
    student_context: Optional[dict] = None  # legacy compat


class ChatResponse(BaseModel):
    reply: str
    suggested_actions: list[str] = []
    sources: list[dict] = []
    agent_data: dict = {}
    session_id: str
    model: str = ""
    retrieved_docs: int = 0


@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="message is required")

    session_id = req.session_id or str(uuid.uuid4())

    # Merge legacy student_context format
    profile = req.student_profile or {}
    if req.student_context and not profile:
        ctx = req.student_context
        profile = {
            "interests": ctx.get("interests", []),
            "skills": ctx.get("skills", []),
            "stream": ctx.get("stream", ""),
            "marks": ctx.get("marks", ""),
        }

    result = await process_chat(
        message=req.message,
        session_id=session_id,
        student_profile=profile or None,
    )
    return ChatResponse(**result)
