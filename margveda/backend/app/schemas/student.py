from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class StudentProfileBase(BaseModel):
    grade: str | None = Field(default=None, max_length=50)
    stream: str | None = Field(default=None, max_length=100)
    interests: str | None = None
    skills: str | None = None
    career_goal: str | None = Field(default=None, max_length=160)
    preferred_location: str | None = Field(default=None, max_length=120)
    budget: str | None = Field(default=None, max_length=80)


class StudentProfileCreate(StudentProfileBase):
    pass


class StudentProfileUpdate(StudentProfileBase):
    pass


class StudentProfileResponse(StudentProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class SessionBookingRequest(BaseModel):
    counsellor_id: int
    topic: str = Field(min_length=3, max_length=180)
    scheduled_at: datetime | None = None
    mode: str = Field(default="online", max_length=40)
    notes: str | None = None


class SessionStatusUpdate(BaseModel):
    status: str = Field(min_length=3, max_length=40)
    notes: str | None = None


class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    counsellor_id: int
    topic: str
    scheduled_at: datetime | None
    mode: str
    status: str
    notes: str | None
    created_at: datetime
    updated_at: datetime


class StudentDashboardResponse(BaseModel):
    profile: StudentProfileResponse | None
    roadmap_count: int
    upcoming_sessions: int
    recommended_next_step: str
