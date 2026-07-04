from app.schemas.chatbot import ChatMessageRequest, ChatMessageResponse, CitationItem
from app.services.ai_client import AIServiceClient

_FALLBACK_REPLY = (
    "I'm here to help you explore careers, colleges, exams, and roadmaps! "
    "Tell me your class, stream, and interests and I'll guide you."
)
_FALLBACK_ACTIONS = [
    "What career should I choose after Class 12 PCM?",
    "Which colleges are best for Computer Science?",
    "How to prepare for JEE in 6 months?",
]


class ChatbotService:
    def __init__(self, ai_client: AIServiceClient | None = None) -> None:
        self.ai_client = ai_client or AIServiceClient()

    async def reply(self, payload: ChatMessageRequest) -> ChatMessageResponse:
        try:
            data = await self.ai_client.post("/chat", {
                "query": payload.message,
                "history": [],
                "student_profile": payload.student_context,
                "domain": None,
            })
            return _parse_ai_response(data)
        except RuntimeError:
            return ChatMessageResponse(reply=_FALLBACK_REPLY, suggested_actions=_FALLBACK_ACTIONS)

    async def public_reply(
        self,
        message: str,
        history: list[dict],
        student_profile: dict | None = None,
        domain: str | None = None,
    ) -> ChatMessageResponse:
        ai_history = [
            {"role": h["role"], "content": h["content"]}
            for h in history
            if h.get("role") in ("user", "assistant") and h.get("content")
        ]
        try:
            data = await self.ai_client.post("/chat", {
                "query": message,
                "history": ai_history,
                "student_profile": student_profile,
                "domain": domain,
            })
            return _parse_ai_response(data)
        except RuntimeError:
            return ChatMessageResponse(reply=_FALLBACK_REPLY, suggested_actions=_FALLBACK_ACTIONS)


def _parse_ai_response(data: dict) -> ChatMessageResponse:
    reply = data.get("answer", _FALLBACK_REPLY)
    suggestions = [s["label"] for s in data.get("suggestions", [])]
    citations = [
        CitationItem(
            index=c["index"],
            title=c["title"],
            domain=c["domain"],
            score=c["score"],
        )
        for c in data.get("citations", [])
    ]
    return ChatMessageResponse(
        reply=reply,
        suggested_actions=suggestions,
        citations=citations,
        needs_counselor=data.get("needs_counselor", False),
        counselor_reason=data.get("counselor_reason", ""),
        from_cache=data.get("from_cache", False),
        latency_ms=data.get("latency_ms", 0),
    )
