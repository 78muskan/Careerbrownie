from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)
    grade = Column(String(50), nullable=True)
    stream = Column(String(100), nullable=True)
    interests = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)
    career_goal = Column(String(160), nullable=True)
    preferred_location = Column(String(120), nullable=True)
    budget = Column(String(80), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="student_profile")
