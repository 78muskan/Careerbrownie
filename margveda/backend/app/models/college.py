from sqlalchemy import JSON, Column, DateTime, Float, Integer, String, func

from app.core.database import Base


class College(Base):
    __tablename__ = "colleges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(220), nullable=False, index=True)
    city = Column(String(120), nullable=False, index=True)
    state = Column(String(120), nullable=False, index=True)
    country = Column(String(120), nullable=False, default="India")
    streams = Column(JSON, nullable=False, default=list)
    courses = Column(JSON, nullable=False, default=list)
    min_score = Column(Integer, nullable=False, default=50)
    entrance_exam = Column(String(80), nullable=True)
    annual_fees = Column(Integer, nullable=True)
    ranking = Column(Integer, nullable=True)
    placement_score = Column(Float, nullable=False, default=0.0)
    website = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
