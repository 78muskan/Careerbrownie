from app.models.schemas import RoadmapMilestone, RoadmapRequest, RoadmapResponse, SkillGapRequest
from app.recommender.skill_gap import SkillGapAnalyzer


class RoadmapPipeline:
    def __init__(self) -> None:
        self.skill_gap = SkillGapAnalyzer()

    def generate(self, payload: RoadmapRequest) -> RoadmapResponse:
        gap = self.skill_gap.analyze(
            SkillGapRequest(
                target_career=payload.target_career,
                current_skills=payload.current_skills,
            )
        )
        skills = gap.missing_skills or gap.existing_skills
        milestones = self._milestones(payload.target_career, skills, payload.timeline_months)
        return RoadmapResponse(
            target_career=payload.target_career,
            summary=f"Personalized {payload.timeline_months}-month path for {payload.target_career}.",
            milestones=milestones,
            skills_to_build=skills,
            resources=["Project courses", "Mentor reviews", "Portfolio examples", "Mock interviews"],
        )

    def _milestones(
        self,
        target_career: str,
        skills: list[str],
        timeline_months: int,
    ) -> list[RoadmapMilestone]:
        titles = ["Explore", "Build", "Showcase", "Prepare"]
        step = max(1, timeline_months // len(titles))
        milestones: list[RoadmapMilestone] = []
        for index, title in enumerate(titles, start=1):
            month = min(timeline_months, index * step)
            selected = skills[index - 1 : index + 1] or skills
            milestones.append(
                RoadmapMilestone(
                    month=month,
                    title=f"{title} {target_career}",
                    goals=[f"Practice {skill}" for skill in selected],
                    deliverable=f"{title} checkpoint reviewed by a counsellor",
                )
            )
        return milestones
