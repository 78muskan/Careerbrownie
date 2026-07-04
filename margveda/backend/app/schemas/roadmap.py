from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RoadmapGenerateRequest(BaseModel):
    target_career: str = Field(min_length=2, max_length=160)
    current_skills: list[str] = Field(default_factory=list)
    timeline_months: int = Field(default=12, ge=3, le=60)


class RoadmapResponse(BaseModel):
    """Serializes a saved CareerRoadmap ORM row."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    title: str
    career_goal: str
    stages: list[dict]
    status: str
    created_at: datetime
    updated_at: datetime
