from fastapi import APIRouter, Depends

from app.api.dependencies import require_roles
from app.models.user import User
from app.schemas.chatbot import ChatMessageRequest, ChatMessageResponse
from app.services.chatbot_service import ChatbotService


router = APIRouter(prefix="/chatbot", tags=["AI Chatbot"])


@router.post("/message", response_model=ChatMessageResponse)
def send_message(
    payload: ChatMessageRequest,
    _: User = Depends(require_roles("student", "counsellor", "admin")),
):
    return ChatbotService().reply(payload)
