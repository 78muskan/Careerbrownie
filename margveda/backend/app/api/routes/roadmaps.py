from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user, get_db, require_roles
from app.models.user import User
from app.schemas.roadmap import RoadmapGenerateRequest, RoadmapResponse
from app.services.roadmap_service import RoadmapService


router = APIRouter(prefix="/roadmaps", tags=["Roadmaps"])


@router.post("/generate", response_model=RoadmapResponse, status_code=201)
def generate_roadmap(
    payload: RoadmapGenerateRequest,
    current_user: User = Depends(require_roles("student")),
    db: Session = Depends(get_db),
):
    return RoadmapService(db).generate_for_student(current_user, payload)


@router.get("/me", response_model=list[RoadmapResponse])
def list_my_roadmaps(
    current_user: User = Depends(require_roles("student")),
    db: Session = Depends(get_db),
):
    return RoadmapService(db).list_for_student(current_user)


@router.get("/{roadmap_id}", response_model=RoadmapResponse)
def read_roadmap(
    roadmap_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    roadmap = RoadmapService(db).get_for_student(current_user, roadmap_id)
    if roadmap is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Roadmap was not found",
        )
    return roadmap
