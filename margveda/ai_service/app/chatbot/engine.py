from app.models.schemas import ChatMessageRequest, ChatMessageResponse


class ChatbotEngine:
    def reply(self, payload: ChatMessageRequest) -> ChatMessageResponse:
        from app.chatbot.bot import chat
        return chat(payload)
