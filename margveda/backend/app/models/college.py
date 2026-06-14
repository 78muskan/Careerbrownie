from sqlalchemy import Column, DateTime, Float, Integer, String, Text, func

from app.core.database import Base


class College(Base):
    __tablename__ = "colleges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(180), nullable=False, index=True)
    location = Column(String(120), nullable=False, index=True)
    courses = Column(Text, nullable=False)
    entrance_exam = Column(String(120), nullable=True)
    fees_min = Column(Integer, nullable=True)
    fees_max = Column(Integer, nullable=True)
    rating = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
