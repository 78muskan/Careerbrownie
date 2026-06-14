from app.schemas.chatbot import ChatMessageRequest, ChatMessageResponse
from app.services.ai_client import AIServiceClient


class ChatbotService:
    def __init__(self, ai_client: AIServiceClient | None = None) -> None:
        self.ai_client = ai_client or AIServiceClient()

    def reply(self, payload: ChatMessageRequest) -> ChatMessageResponse:
        try:
            data = self.ai_client.post("/chatbot/chat", payload.model_dump())
            return ChatMessageResponse(**data)
        except RuntimeError:
            return ChatMessageResponse(
                reply=(
                    "I can help you explore careers, skills, colleges, and roadmaps. "
                    "Tell me your class, stream, interests, and the careers you are curious about."
                ),
                suggested_actions=[
                    "Complete your student profile",
                    "Generate career recommendations",
                    "Create a career roadmap",
                ],
            )
