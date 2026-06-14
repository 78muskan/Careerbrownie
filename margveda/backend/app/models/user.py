from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(30), nullable=False, default="student")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    student_profile = relationship(
        "StudentProfile",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )
    counsellor_profile = relationship(
        "CounsellorProfile",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )
    student_sessions = relationship(
        "GuidanceSession",
        back_populates="student",
        foreign_keys="GuidanceSession.student_id",
    )
    counsellor_sessions = relationship(
        "GuidanceSession",
        back_populates="counsellor",
        foreign_keys="GuidanceSession.counsellor_id",
    )
    roadmaps = relationship(
        "CareerRoadmap",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    student_profile = relationship(
        "Student",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    counsellor_profile = relationship(
        "Counsellor",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    booked_sessions = relationship(
        "SessionBooking",
        foreign_keys="SessionBooking.student_id",
        back_populates="student",
    )
    assigned_sessions = relationship(
        "SessionBooking",
        foreign_keys="SessionBooking.counsellor_id",
        back_populates="counsellor",
    )
    roadmaps = relationship(
        "CareerRoadmap",
        back_populates="student",
        cascade="all, delete-orphan",
    )
