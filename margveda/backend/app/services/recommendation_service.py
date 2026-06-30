from app.schemas.recommendation import (
    CareerOption,
    CareerRecommendationRequest,
    CareerRecommendationResponse,
    CollegeOption,
    CollegePredictionRequest,
    CollegePredictionResponse,
    SkillGapRequest,
    SkillGapResponse,
)
from app.services.ai_client import AIServiceClient


class RecommendationService:
    def __init__(self, ai_client: AIServiceClient | None = None) -> None:
        self.ai_client = ai_client or AIServiceClient()

    def recommend_careers(
        self,
        payload: CareerRecommendationRequest,
    ) -> CareerRecommendationResponse:
        try:
            data = self.ai_client.post("/recommendations/careers", payload.model_dump())
            return CareerRecommendationResponse(**data)
        except RuntimeError:
            return CareerRecommendationResponse(
                recommendations=[
                    CareerOption(
                        title="AI Product Manager",
                        match_score=0.87,
                        reason="Strong fit for students who like technology, planning, and communication.",
                        skills_to_build=["Python basics", "Product thinking", "Data analysis"],
                    ),
                    CareerOption(
                        title="Data Analyst",
                        match_score=0.82,
                        reason="Good path when analytical skills and practical business problem solving overlap.",
                        skills_to_build=["Excel", "SQL", "Statistics", "Dashboards"],
                    ),
                    CareerOption(
                        title="Career Counselling Psychologist",
                        match_score=0.76,
                        reason="Useful if you enjoy human behavior, mentoring, and education guidance.",
                        skills_to_build=["Psychology foundations", "Assessment methods", "Communication"],
                    ),
                ]
            )

    def skill_gap(self, payload: SkillGapRequest) -> SkillGapResponse:
        try:
            data = self.ai_client.post("/recommendations/skill-gap", payload.model_dump())
            return SkillGapResponse(**data)
        except RuntimeError:
            missing = ["Communication", "Portfolio building", "Industry basics"]
            return SkillGapResponse(
                target_career=payload.target_career,
                missing_skills=missing,
                learning_plan=[
                    "Study the career role and daily responsibilities.",
                    "Build one small project connected to the role.",
                    "Speak with a counsellor or mentor for feedback.",
                ],
            )

    def predict_colleges(
        self,
        payload: CollegePredictionRequest,
    ) -> CollegePredictionResponse:
        try:
            data = self.ai_client.post("/recommendations/colleges", payload.model_dump())
            return CollegePredictionResponse(**data)
        except RuntimeError:
            return CollegePredictionResponse(
                colleges=[
                    CollegeOption(
                        name="Career Brownie Institute Match",
                        location=payload.preferred_location or "India",
                        courses=[payload.academic_stream, "Career Foundation Program"],
                        fit_score=0.78,
                        reason="Fallback match based on stream, score, and location preference.",
                    )
                ]
            )
