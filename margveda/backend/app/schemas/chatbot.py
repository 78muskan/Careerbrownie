from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    message: str = Field(min_length=2, max_length=2000)
    student_context: dict | None = None


class ChatMessageResponse(BaseModel):
    reply: str
    suggested_actions: list[str] = []
