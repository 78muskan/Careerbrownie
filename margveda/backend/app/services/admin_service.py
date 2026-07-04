from sqlalchemy.orm import Session

from app.models.college import College
from app.models.counsellor import CounsellorProfile
from app.models.roadmap import CareerRoadmap
from app.models.session import GuidanceSession
from app.models.student import StudentProfile
from app.models.user import User


class AdminService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def dashboard(self) -> dict:
        return {
            "total_users": self.db.query(User).count(),
            "students": self.db.query(StudentProfile).count(),
            "counsellors": self.db.query(CounsellorProfile).count(),
            "sessions": self.db.query(GuidanceSession).count(),
            "roadmaps": self.db.query(CareerRoadmap).count(),
            "colleges": self.db.query(College).count(),
        }

    def list_users(self) -> list[User]:
        return self.db.query(User).order_by(User.created_at.desc()).all()

    def set_user_active(self, user_id: int, is_active: bool) -> User | None:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            return None
        user.is_active = is_active
        self.db.commit()
        self.db.refresh(user)
        return user
