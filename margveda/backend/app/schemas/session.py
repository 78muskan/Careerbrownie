from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class SessionStatus(str, Enum):
    requested = "requested"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"


class SessionMode(str, Enum):
    video = "video"
    phone = "phone"
    in_person = "in_person"


class SessionCreate(BaseModel):
    counsellor_id: int
    scheduled_at: datetime
    duration_minutes: int = Field(default=45, ge=15, le=180)
    mode: SessionMode = SessionMode.video
    topic: str = Field(min_length=3, max_length=180)
    notes: str | None = None


class SessionStatusUpdate(BaseModel):
    status: SessionStatus
    meeting_link: str | None = Field(default=None, max_length=255)
    notes: str | None = None


class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    counsellor_id: int
    scheduled_at: datetime
    duration_minutes: int
    mode: SessionMode
    status: SessionStatus
    topic: str
    notes: str | None
    meeting_link: str | None
    created_at: datetime
    updated_at: datetime
