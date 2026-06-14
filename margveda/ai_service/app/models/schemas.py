from pydantic import BaseModel, Field


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
    target_career: str


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
    career_goal: str
    current_level: str | None = None
    timeline_months: int = 12


class RoadmapResponse(BaseModel):
    title: str
    career_goal: str
    stages: list[RoadmapStage]


class ChatMessageRequest(BaseModel):
    message: str
    student_context: dict | None = None


class ChatMessageResponse(BaseModel):
    reply: str
    suggested_actions: list[str] = []
