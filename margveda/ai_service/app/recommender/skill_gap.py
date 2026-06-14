from app.models.schemas import SkillGapRequest, SkillGapResponse
from app.recommender.career_recommender import CareerRecommender


class SkillGapAnalyzer:
    def __init__(self) -> None:
        self.recommender = CareerRecommender()

    def analyze(self, payload: SkillGapRequest) -> SkillGapResponse:
        required = self.recommender.skills_for(payload.target_career)
        current = {skill.strip().lower() for skill in payload.current_skills}
        existing = [skill for skill in required if skill.lower() in current]
        missing = [skill for skill in required if skill.lower() not in current]
        plan = [
            f"Build one practical mini-project focused on {skill}"
            for skill in missing[:5]
        ]
        if not plan:
            plan.append("Move into portfolio projects and mock interviews")
        return SkillGapResponse(
            target_career=payload.target_career,
            existing_skills=existing,
            missing_skills=missing,
            learning_plan=plan,
        )
