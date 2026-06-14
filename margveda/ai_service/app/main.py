from fastapi import FastAPI

from app.chatbot.bot import chat
from app.models.schemas import (
    CareerRecommendationRequest,
    CareerRecommendationResponse,
    ChatMessageRequest,
    ChatMessageResponse,
    CollegePredictionRequest,
    CollegePredictionResponse,
    RoadmapRequest,
    RoadmapResponse,
    SkillGapRequest,
    SkillGapResponse,
)
from app.pipelines.college_prediction import predict_colleges
from app.pipelines.skill_gap import analyze_skill_gap
from app.recommender.engine import recommend_careers
from app.roadmap.generator import generate_roadmap


app = FastAPI(
    title="MargVedA AI Service",
    version="1.0.0",
    description="Python AI service for career recommendations, roadmap planning, and chatbot assistance.",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ai_service"}


@app.post("/chatbot/chat", response_model=ChatMessageResponse)
def chatbot_chat(payload: ChatMessageRequest):
    return chat(payload)


@app.post("/recommendations/careers", response_model=CareerRecommendationResponse)
def career_recommendations(payload: CareerRecommendationRequest):
    return recommend_careers(payload)


@app.post("/recommendations/skill-gap", response_model=SkillGapResponse)
def skill_gap(payload: SkillGapRequest):
    return analyze_skill_gap(payload)


@app.post("/recommendations/colleges", response_model=CollegePredictionResponse)
def colleges(payload: CollegePredictionRequest):
    return predict_colleges(payload)


@app.post("/roadmaps/generate", response_model=RoadmapResponse)
def roadmaps(payload: RoadmapRequest):
    return generate_roadmap(payload)
