from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.session import GuidanceSession
from app.models.user import User
from app.schemas.session import SessionCreate, SessionStatusUpdate


class SessionService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def book_session(self, student: User, payload: SessionCreate) -> GuidanceSession:
        if student.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can book counselling sessions",
            )

        counsellor = (
            self.db.query(User)
            .filter(
                User.id == payload.counsellor_id,
                User.role == "counsellor",
                User.is_active.is_(True),
            )
            .first()
        )
        if counsellor is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Counsellor was not found",
            )

        self._ensure_future_time(payload.scheduled_at)
        booking = GuidanceSession(
            student_id=student.id,
            counsellor_id=counsellor.id,
            scheduled_at=payload.scheduled_at,
            duration_minutes=payload.duration_minutes,
            mode=payload.mode.value,
            topic=payload.topic,
            notes=payload.notes,
        )
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def list_for_user(self, user: User) -> list[GuidanceSession]:
        query = self.db.query(GuidanceSession)
        if user.role == "student":
            query = query.filter(GuidanceSession.student_id == user.id)
        elif user.role == "counsellor":
            query = query.filter(GuidanceSession.counsellor_id == user.id)
        elif user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unsupported role",
            )
        return query.order_by(GuidanceSession.scheduled_at.desc()).all()

    def update_status(
        self,
        session_id: int,
        actor: User,
        payload: SessionStatusUpdate,
    ) -> GuidanceSession:
        booking = self.db.query(GuidanceSession).filter(GuidanceSession.id == session_id).first()
        if booking is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session was not found",
            )

        is_owner = booking.student_id == actor.id or booking.counsellor_id == actor.id
        if actor.role != "admin" and not is_owner:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this session",
            )

        booking.status = payload.status.value
        if payload.meeting_link is not None:
            booking.meeting_link = payload.meeting_link
        if payload.notes is not None:
            booking.notes = payload.notes

        self.db.commit()
        self.db.refresh(booking)
        return booking

    def _ensure_future_time(self, scheduled_at: datetime) -> None:
        now = (
            datetime.now(scheduled_at.tzinfo)
            if scheduled_at.tzinfo is not None
            else datetime.now(timezone.utc).replace(tzinfo=None)
        )
        if scheduled_at <= now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session time must be in the future",
            )
