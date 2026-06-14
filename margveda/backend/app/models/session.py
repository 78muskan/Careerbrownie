from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class GuidanceSession(Base):
    __tablename__ = "guidance_sessions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    counsellor_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    topic = Column(String(180), nullable=False)
    scheduled_at = Column(DateTime(timezone=True), nullable=True, index=True)
    mode = Column(String(40), nullable=False, default="online")
    status = Column(String(40), nullable=False, default="requested", index=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    student = relationship(
        "User",
        back_populates="student_sessions",
        foreign_keys=[student_id],
    )
    counsellor = relationship(
        "User",
        back_populates="counsellor_sessions",
        foreign_keys=[counsellor_id],
    )
