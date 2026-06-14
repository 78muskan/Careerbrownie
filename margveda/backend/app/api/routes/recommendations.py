from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, require_roles
from app.models.user import User
from app.schemas.recommendation import (
    CareerRecommendationRequest,
    CareerRecommendationResponse,
    CollegePredictionRequest,
    CollegePredictionResponse,
    RoadmapRequest,
    SavedRoadmapResponse,
    SkillGapRequest,
    SkillGapResponse,
)
from app.services.recommendation_service import RecommendationService
from app.services.roadmap_service import RoadmapService


router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.post("/careers", response_model=CareerRecommendationResponse)
def recommend_careers(
    payload: CareerRecommendationRequest,
    _: User = Depends(require_roles("student", "counsellor", "admin")),
):
    return RecommendationService().recommend_careers(payload)


@router.post("/skill-gap", response_model=SkillGapResponse)
def analyze_skill_gap(
    payload: SkillGapRequest,
    _: User = Depends(require_roles("student", "counsellor", "admin")),
):
    return RecommendationService().skill_gap(payload)


@router.post("/colleges", response_model=CollegePredictionResponse)
def predict_colleges(
    payload: CollegePredictionRequest,
    _: User = Depends(require_roles("student", "counsellor", "admin")),
):
    return RecommendationService().predict_colleges(payload)


@router.post(
    "/roadmaps",
    response_model=SavedRoadmapResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_roadmap(
    payload: RoadmapRequest,
    current_user: User = Depends(require_roles("student")),
    db: Session = Depends(get_db),
):
    return RoadmapService(db).generate_and_save(current_user, payload)


@router.get("/roadmaps", response_model=list[SavedRoadmapResponse])
def list_roadmaps(
    current_user: User = Depends(require_roles("student", "admin")),
    db: Session = Depends(get_db),
):
    return RoadmapService(db).list_for_student(current_user)
