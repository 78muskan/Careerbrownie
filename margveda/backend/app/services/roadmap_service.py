from sqlalchemy.orm import Session

from app.models.roadmap import CareerRoadmap
from app.models.user import User
from app.schemas.recommendation import RoadmapRequest, RoadmapResponse, RoadmapStage
from app.schemas.roadmap import RoadmapGenerateRequest
from app.services.ai_client import AIServiceClient


class RoadmapService:
    def __init__(self, db: Session, ai_client: AIServiceClient | None = None) -> None:
        self.db = db
        self.ai_client = ai_client or AIServiceClient()

    # ── Internal AI generation (no DB) ──────────────────────────────────────

    def generate(self, payload: RoadmapRequest) -> RoadmapResponse:
        """Call AI service; fall back to a structured default on failure."""
        try:
            data = self.ai_client.post("/roadmaps/generate", payload.model_dump())
            return RoadmapResponse(**data)
        except RuntimeError:
            return RoadmapResponse(
                title=f"{payload.career_goal} Roadmap",
                career_goal=payload.career_goal,
                stages=[
                    RoadmapStage(
                        title="Foundation",
                        description="Understand the role, required skills, and entry paths.",
                        duration="1-2 months",
                        resources=["Intro videos", "Career articles", "Counsellor discussion"],
                    ),
                    RoadmapStage(
                        title="Skill Building",
                        description="Build core technical, academic, and communication skills.",
                        duration="3-6 months",
                        resources=["Online courses", "Practice projects", "Peer review"],
                    ),
                    RoadmapStage(
                        title="Portfolio and Applications",
                        description="Prepare proof of work, college applications, or internships.",
                        duration="2-4 months",
                        resources=["Resume", "Project portfolio", "Mock interviews"],
                    ),
                ],
            )

    # ── Persist via recommendations route (RoadmapRequest input) ───────────

    def generate_and_save(self, user: User, payload: RoadmapRequest) -> CareerRoadmap:
        """Used by /recommendations/roadmaps — takes RoadmapRequest."""
        roadmap = self.generate(payload)
        record = CareerRoadmap(
            student_id=user.id,
            career_goal=roadmap.career_goal,
            title=roadmap.title,
            stages=[stage.model_dump() for stage in roadmap.stages],
            status="active",
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    # ── Persist via roadmaps route (RoadmapGenerateRequest input) ──────────

    def generate_for_student(
        self, user: User, payload: RoadmapGenerateRequest
    ) -> CareerRoadmap:
        """Used by /roadmaps/generate — takes RoadmapGenerateRequest."""
        fallback_stages = [
            {
                "title": "Foundation",
                "description": f"Understand what {payload.target_career} involves day-to-day.",
                "duration": "1-2 months",
                "resources": ["Career articles", "YouTube overviews", "LinkedIn profiles"],
            },
            {
                "title": "Skill Building",
                "description": "Acquire the core skills required for entry-level roles.",
                "duration": "3-6 months",
                "resources": ["Online courses", "Side projects", "Open-source contributions"],
            },
            {
                "title": "Portfolio and Applications",
                "description": "Build evidence of your skills and apply to roles or colleges.",
                "duration": "2-4 months",
                "resources": ["GitHub portfolio", "Resume", "Mock interviews"],
            },
        ]

        try:
            data = self.ai_client.post(
                "/roadmaps/generate",
                {
                    "career_goal": payload.target_career,
                    "current_level": ", ".join(payload.current_skills) if payload.current_skills else None,
                    "timeline_months": payload.timeline_months,
                },
            )
            stages = data.get("stages", fallback_stages)
            # Normalise: stages may arrive as dicts or Pydantic models
            stages = [s if isinstance(s, dict) else s.model_dump() for s in stages]
        except RuntimeError:
            stages = fallback_stages

        record = CareerRoadmap(
            student_id=user.id,
            career_goal=payload.target_career,
            title=f"{payload.target_career} Roadmap ({payload.timeline_months} months)",
            stages=stages,
            status="active",
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_for_student(self, user: User, roadmap_id: int) -> CareerRoadmap | None:
        return (
            self.db.query(CareerRoadmap)
            .filter(
                CareerRoadmap.id == roadmap_id,
                CareerRoadmap.student_id == user.id,
            )
            .first()
        )

    def list_for_student(self, user: User) -> list[CareerRoadmap]:
        return (
            self.db.query(CareerRoadmap)
            .filter(CareerRoadmap.student_id == user.id)
            .order_by(CareerRoadmap.created_at.desc())
            .all()
        )
