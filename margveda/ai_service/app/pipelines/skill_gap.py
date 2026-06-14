from app.models.schemas import SkillGapRequest, SkillGapResponse


CAREER_SKILL_MAP = {
    "ai engineer": ["Python", "Machine learning", "APIs", "Data structures", "Math"],
    "data analyst": ["SQL", "Excel", "Statistics", "Dashboards", "Business thinking"],
    "ux designer": ["User research", "Wireframing", "Prototyping", "Design systems"],
    "doctor": ["Biology", "Chemistry", "Physics", "NEET practice", "Patient empathy"],
    "chartered accountant": ["Accounting", "Taxation", "Audit", "Business law"],
}


def analyze_skill_gap(payload: SkillGapRequest) -> SkillGapResponse:
    target = payload.target_career.lower()
    required = CAREER_SKILL_MAP.get(
        target,
        ["Communication", "Problem solving", "Portfolio building", "Domain fundamentals"],
    )
    current = {skill.lower() for skill in payload.current_skills}
    missing = [skill for skill in required if skill.lower() not in current]

    return SkillGapResponse(
        target_career=payload.target_career,
        missing_skills=missing,
        learning_plan=[
            f"Learn {skill} with a beginner project or practice routine."
            for skill in missing[:5]
        ]
        or ["You already cover the core skills. Start building portfolio proof."],
    )
