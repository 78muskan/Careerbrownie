from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    message: str = Field(min_length=2, max_length=2000)
    student_context: dict | None = None


class CitationItem(BaseModel):
    index: int
    title: str
    domain: str
    score: float


class ChatMessageResponse(BaseModel):
    reply: str
    suggested_actions: list[str] = []
    citations: list[CitationItem] = []
    needs_counselor: bool = False
    counselor_reason: str = ""
    from_cache: bool = False
    latency_ms: int = 0
