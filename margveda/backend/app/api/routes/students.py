from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, require_roles
from app.models.user import User
from app.schemas.session import SessionResponse
from app.schemas.student import (
    SessionBookingRequest,
    StudentDashboardResponse,
    StudentProfileResponse,
    StudentProfileUpdate,
)
from app.services.student_service import StudentService


router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/me", response_model=StudentProfileResponse)
def get_my_profile(
    current_user: User = Depends(require_roles("student", "admin")),
    db: Session = Depends(get_db),
):
    return StudentService(db).get_or_create_profile(current_user)


@router.put("/me", response_model=StudentProfileResponse)
def update_my_profile(
    payload: StudentProfileUpdate,
    current_user: User = Depends(require_roles("student", "admin")),
    db: Session = Depends(get_db),
):
    return StudentService(db).update_profile(current_user, payload)


@router.get("/dashboard", response_model=StudentDashboardResponse)
def get_dashboard(
    current_user: User = Depends(require_roles("student", "admin")),
    db: Session = Depends(get_db),
):
    return StudentService(db).get_dashboard(current_user)


@router.post(
    "/sessions",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def book_session(
    payload: SessionBookingRequest,
    current_user: User = Depends(require_roles("student")),
    db: Session = Depends(get_db),
):
    return StudentService(db).book_session(current_user, payload)
