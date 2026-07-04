from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.session import SessionResponse


class CounsellorProfileBase(BaseModel):
    specialization: str | None = Field(default=None, max_length=160)
    bio: str | None = None
    years_experience: int = Field(default=0, ge=0, le=60)
    availability: str | None = Field(default=None, max_length=255)


class CounsellorProfileCreate(CounsellorProfileBase):
    pass


class CounsellorProfileUpdate(CounsellorProfileBase):
    pass


class CounsellorProfileResponse(CounsellorProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    rating: float
    created_at: datetime
    updated_at: datetime


class CounsellorDashboardResponse(BaseModel):
    profile: CounsellorProfileResponse | None
    total_sessions: int
    requested_sessions: int
    upcoming_sessions: list[SessionResponse]
