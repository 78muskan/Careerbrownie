from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.api.dependencies import require_roles
from app.models.user import User
from app.schemas.chatbot import ChatMessageRequest, ChatMessageResponse
from app.services.chatbot_service import ChatbotService


router = APIRouter(prefix="/chatbot", tags=["AI Chatbot"])


# ── Authenticated endpoint (student / counsellor dashboard) ──────────────────

@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    payload: ChatMessageRequest,
    _: User = Depends(require_roles("student", "counsellor", "admin")),
):
    return await ChatbotService().reply(payload)


# ── Public endpoint (floating chat widget — no login required) ───────────────

class PublicChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    history: list[dict] = Field(default_factory=list, max_length=20)
    student_profile: dict | None = None
    domain: str | None = None


@router.post("/public-chat", response_model=ChatMessageResponse)
async def public_chat(payload: PublicChatRequest):
    """
    Unauthenticated chat endpoint for the floating ChatWidget on the website.

    Forwards the request to the AI service and returns a reply + suggested actions.
    Falls back to a helpful static message if the AI service is unreachable.
    """
    return await ChatbotService().public_reply(
        message=payload.message,
        history=payload.history,
        student_profile=payload.student_profile,
        domain=payload.domain,
    )
