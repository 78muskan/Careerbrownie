from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CareerRecommendationRequest(BaseModel):
    interests: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    academic_stream: str | None = None
    preferred_location: str | None = None


class CareerOption(BaseModel):
    title: str
    match_score: float
    reason: str
    skills_to_build: list[str] = []


class CareerRecommendationResponse(BaseModel):
    recommendations: list[CareerOption]


class SkillGapRequest(BaseModel):
    current_skills: list[str] = Field(default_factory=list)
    target_career: str = Field(min_length=2, max_length=180)


class SkillGapResponse(BaseModel):
    target_career: str
    missing_skills: list[str]
    learning_plan: list[str]


class CollegePredictionRequest(BaseModel):
    academic_stream: str
    score_percent: float = Field(ge=0, le=100)
    preferred_location: str | None = None
    budget: str | None = None


class CollegeOption(BaseModel):
    name: str
    location: str
    courses: list[str]
    fit_score: float
    reason: str


class CollegePredictionResponse(BaseModel):
    colleges: list[CollegeOption]


class RoadmapStage(BaseModel):
    title: str
    description: str
    duration: str
    resources: list[str] = []


class RoadmapRequest(BaseModel):
    career_goal: str = Field(min_length=2, max_length=180)
    current_level: str | None = None
    timeline_months: int = Field(default=12, ge=1, le=60)


class RoadmapResponse(BaseModel):
    title: str
    career_goal: str
    stages: list[RoadmapStage]


class SavedRoadmapResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    career_goal: str
    title: str
    stages: list[dict]
    status: str
    created_at: datetime
    updated_at: datetime
