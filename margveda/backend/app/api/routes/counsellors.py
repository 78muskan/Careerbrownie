from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, require_roles
from app.models.user import User
from app.schemas.counsellor import (
    CounsellorDashboardResponse,
    CounsellorProfileResponse,
    CounsellorProfileUpdate,
)
from app.schemas.session import SessionResponse, SessionStatusUpdate
from app.services.counsellor_service import CounsellorService


router = APIRouter(prefix="/counsellors", tags=["Counsellors"])


@router.get("/me", response_model=CounsellorProfileResponse)
def get_my_profile(
    current_user: User = Depends(require_roles("counsellor", "admin")),
    db: Session = Depends(get_db),
):
    return CounsellorService(db).get_or_create_profile(current_user)


@router.put("/me", response_model=CounsellorProfileResponse)
def update_my_profile(
    payload: CounsellorProfileUpdate,
    current_user: User = Depends(require_roles("counsellor", "admin")),
    db: Session = Depends(get_db),
):
    return CounsellorService(db).update_profile(current_user, payload)


@router.get("/dashboard", response_model=CounsellorDashboardResponse)
def get_dashboard(
    current_user: User = Depends(require_roles("counsellor", "admin")),
    db: Session = Depends(get_db),
):
    return CounsellorService(db).get_dashboard(current_user)


@router.get("/sessions", response_model=list[SessionResponse])
def list_sessions(
    current_user: User = Depends(require_roles("counsellor", "admin")),
    db: Session = Depends(get_db),
):
    return CounsellorService(db).list_sessions(current_user)


@router.patch("/sessions/{session_id}", response_model=SessionResponse)
def update_session_status(
    session_id: int,
    payload: SessionStatusUpdate,
    current_user: User = Depends(require_roles("counsellor")),
    db: Session = Depends(get_db),
):
    return CounsellorService(db).update_session_status(current_user, session_id, payload)
