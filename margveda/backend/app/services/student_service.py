from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.counsellor import CounsellorProfile
from app.models.roadmap import CareerRoadmap
from app.models.session import GuidanceSession
from app.models.student import StudentProfile
from app.models.user import User
from app.schemas.student import (
    SessionBookingRequest,
    StudentDashboardResponse,
    StudentProfileUpdate,
)


class StudentService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_or_create_profile(self, user: User) -> StudentProfile:
        profile = user.student_profile
        if profile is None:
            profile = StudentProfile(user_id=user.id)
            self.db.add(profile)
            self.db.commit()
            self.db.refresh(profile)
        return profile

    def update_profile(self, user: User, payload: StudentProfileUpdate) -> StudentProfile:
        profile = self.get_or_create_profile(user)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(profile, field, value)

        self.db.commit()
        self.db.refresh(profile)
        return profile

    def get_dashboard(self, user: User) -> StudentDashboardResponse:
        profile = self.get_or_create_profile(user)
        roadmap_count = (
            self.db.query(CareerRoadmap)
            .filter(CareerRoadmap.student_id == user.id)
            .count()
        )
        upcoming_sessions = (
            self.db.query(GuidanceSession)
            .filter(
                GuidanceSession.student_id == user.id,
                GuidanceSession.status.in_(["requested", "confirmed"]),
            )
            .count()
        )
        next_step = "Complete your profile to unlock stronger recommendations."
        if profile.career_goal:
            next_step = f"Generate a roadmap for {profile.career_goal}."

        return StudentDashboardResponse(
            profile=profile,
            roadmap_count=roadmap_count,
            upcoming_sessions=upcoming_sessions,
            recommended_next_step=next_step,
        )

    def book_session(self, user: User, payload: SessionBookingRequest) -> GuidanceSession:
        counsellor = (
            self.db.query(User)
            .join(CounsellorProfile, CounsellorProfile.user_id == User.id)
            .filter(User.id == payload.counsellor_id, User.role == "counsellor")
            .first()
        )
        if counsellor is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Counsellor not found",
            )

        session = GuidanceSession(
            student_id=user.id,
            counsellor_id=counsellor.id,
            topic=payload.topic,
            scheduled_at=payload.scheduled_at,
            mode=payload.mode,
            notes=payload.notes,
            status="requested",
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session
