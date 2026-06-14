from sqlalchemy.orm import Session

from app.models.roadmap import CareerRoadmap
from app.models.user import User
from app.schemas.recommendation import RoadmapRequest, RoadmapResponse, RoadmapStage
from app.services.ai_client import AIServiceClient


class RoadmapService:
    def __init__(self, db: Session, ai_client: AIServiceClient | None = None) -> None:
        self.db = db
        self.ai_client = ai_client or AIServiceClient()

    def generate(self, payload: RoadmapRequest) -> RoadmapResponse:
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

    def generate_and_save(self, user: User, payload: RoadmapRequest) -> CareerRoadmap:
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

    def list_for_student(self, user: User) -> list[CareerRoadmap]:
        return (
            self.db.query(CareerRoadmap)
            .filter(CareerRoadmap.student_id == user.id)
            .order_by(CareerRoadmap.created_at.desc())
            .all()
        )
