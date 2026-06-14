from app.models.schemas import (
    CareerOption,
    CareerRecommendationRequest,
    CareerRecommendationResponse,
)


CAREER_LIBRARY = [
    {
        "title": "AI Engineer",
        "keywords": {"python", "math", "ai", "machine learning", "coding", "data"},
        "skills": ["Python", "Linear algebra", "Machine learning", "APIs"],
    },
    {
        "title": "Data Analyst",
        "keywords": {"excel", "statistics", "business", "data", "analytics", "math"},
        "skills": ["SQL", "Excel", "Statistics", "Data visualization"],
    },
    {
        "title": "UX Designer",
        "keywords": {"design", "psychology", "creativity", "research", "apps"},
        "skills": ["User research", "Wireframing", "Design systems", "Communication"],
    },
    {
        "title": "Doctor",
        "keywords": {"biology", "healthcare", "medicine", "science", "helping"},
        "skills": ["Biology", "Chemistry", "Patient communication", "NEET preparation"],
    },
    {
        "title": "Chartered Accountant",
        "keywords": {"commerce", "accounts", "finance", "tax", "business"},
        "skills": ["Accounting", "Taxation", "Audit basics", "Financial reporting"],
    },
    {
        "title": "Career Counsellor",
        "keywords": {"psychology", "teaching", "mentoring", "education", "guidance"},
        "skills": ["Psychology", "Counselling methods", "Assessments", "Empathy"],
    },
]


def recommend_careers(payload: CareerRecommendationRequest) -> CareerRecommendationResponse:
    student_words = set()
    for item in payload.interests + payload.skills:
        student_words.update(item.lower().replace(",", " ").split())
    if payload.academic_stream:
        student_words.update(payload.academic_stream.lower().split())

    recommendations: list[CareerOption] = []
    for career in CAREER_LIBRARY:
        overlap = len(student_words.intersection(career["keywords"]))
        score = min(0.95, 0.55 + (overlap * 0.1))
        if overlap == 0 and recommendations:
            score = 0.52

        recommendations.append(
            CareerOption(
                title=career["title"],
                match_score=round(score, 2),
                reason=(
                    f"Matches your interests in {', '.join(sorted(student_words)[:4]) or 'career exploration'} "
                    f"and can grow into a practical student roadmap."
                ),
                skills_to_build=career["skills"],
            )
        )

    recommendations.sort(key=lambda item: item.match_score, reverse=True)
    return CareerRecommendationResponse(recommendations=recommendations[:5])
