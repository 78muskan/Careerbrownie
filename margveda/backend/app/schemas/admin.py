from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.auth import UserRole


class AdminOverviewResponse(BaseModel):
    users: int
    students: int
    counsellors: int
    sessions: int
    roadmaps: int
    colleges: int


class UserAdminResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime


class UserStatusUpdate(BaseModel):
    is_active: bool


class CollegeBase(BaseModel):
    name: str = Field(min_length=2, max_length=220)
    city: str = Field(min_length=2, max_length=120)
    state: str = Field(min_length=2, max_length=120)
    country: str = Field(default="India", max_length=120)
    streams: list[str] = Field(default_factory=list)
    courses: list[str] = Field(default_factory=list)
    min_score: int = Field(default=50, ge=0, le=100)
    entrance_exam: str | None = Field(default=None, max_length=80)
    annual_fees: int | None = Field(default=None, ge=0)
    ranking: int | None = Field(default=None, ge=1)
    placement_score: float = Field(default=0.0, ge=0, le=10)
    website: str | None = Field(default=None, max_length=255)


class CollegeCreate(CollegeBase):
    pass


class CollegeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=220)
    city: str | None = Field(default=None, min_length=2, max_length=120)
    state: str | None = Field(default=None, min_length=2, max_length=120)
    country: str | None = Field(default=None, max_length=120)
    streams: list[str] | None = None
    courses: list[str] | None = None
    min_score: int | None = Field(default=None, ge=0, le=100)
    entrance_exam: str | None = Field(default=None, max_length=80)
    annual_fees: int | None = Field(default=None, ge=0)
    ranking: int | None = Field(default=None, ge=1)
    placement_score: float | None = Field(default=None, ge=0, le=10)
    website: str | None = Field(default=None, max_length=255)


class CollegeResponse(CollegeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
