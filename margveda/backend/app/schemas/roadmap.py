from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RoadmapGenerateRequest(BaseModel):
    target_career: str = Field(min_length=2, max_length=160)
    current_skills: list[str] = Field(default_factory=list)
    timeline_months: int = Field(default=12, ge=3, le=60)


class RoadmapMilestone(BaseModel):
    month: int
    title: str
    goals: list[str]
    deliverable: str


class RoadmapResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    title: str
    target_career: str
    summary: str
    milestones: list[RoadmapMilestone]
    skills_to_build: list[str]
    resources: list[str]
    estimated_months: int
    generated_by: str
    created_at: datetime
    updated_at: datetime
