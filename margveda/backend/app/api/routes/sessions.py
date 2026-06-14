from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user, get_db, require_roles
from app.models.user import User
from app.schemas.session import SessionCreate, SessionResponse, SessionStatusUpdate
from app.services.session_service import SessionService


router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post("/book", response_model=SessionResponse, status_code=201)
def book_session(
    payload: SessionCreate,
    current_user: User = Depends(require_roles("student")),
    db: Session = Depends(get_db),
):
    return SessionService(db).book_session(current_user, payload)


@router.get("/me", response_model=list[SessionResponse])
def list_my_sessions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return SessionService(db).list_for_user(current_user)


@router.patch("/{session_id}/status", response_model=SessionResponse)
def update_session_status(
    session_id: int,
    payload: SessionStatusUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return SessionService(db).update_status(session_id, current_user, payload)
