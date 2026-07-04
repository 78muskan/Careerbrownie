from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.counsellor import CounsellorProfile
from app.models.session import GuidanceSession
from app.models.user import User
from app.schemas.counsellor import CounsellorDashboardResponse, CounsellorProfileUpdate
from app.schemas.session import SessionStatusUpdate


class CounsellorService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_or_create_profile(self, user: User) -> CounsellorProfile:
        profile = user.counsellor_profile
        if profile is None:
            profile = CounsellorProfile(user_id=user.id)
            self.db.add(profile)
            self.db.commit()
            self.db.refresh(profile)
        return profile

    def update_profile(self, user: User, payload: CounsellorProfileUpdate) -> CounsellorProfile:
        profile = self.get_or_create_profile(user)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(profile, field, value)

        self.db.commit()
        self.db.refresh(profile)
        return profile

    def list_sessions(self, user: User) -> list[GuidanceSession]:
        return (
            self.db.query(GuidanceSession)
            .filter(GuidanceSession.counsellor_id == user.id)
            .order_by(GuidanceSession.created_at.desc())
            .all()
        )

    def get_dashboard(self, user: User) -> CounsellorDashboardResponse:
        profile = self.get_or_create_profile(user)
        sessions = self.list_sessions(user)
        requested = [s for s in sessions if s.status == "requested"]
        upcoming = [s for s in sessions if s.status in {"requested", "confirmed"}][:5]
        return CounsellorDashboardResponse(
            profile=profile,
            total_sessions=len(sessions),
            requested_sessions=len(requested),
            upcoming_sessions=upcoming,
        )

    def update_session_status(
        self,
        user: User,
        session_id: int,
        payload: SessionStatusUpdate,
    ) -> GuidanceSession:
        session = (
            self.db.query(GuidanceSession)
            .filter(
                GuidanceSession.id == session_id,
                GuidanceSession.counsellor_id == user.id,
            )
            .first()
        )
        if session is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found",
            )

        session.status = payload.status.value
        if payload.meeting_link is not None:
            session.meeting_link = payload.meeting_link
        if payload.notes is not None:
            session.notes = payload.notes
        self.db.commit()
        self.db.refresh(session)
        return session
