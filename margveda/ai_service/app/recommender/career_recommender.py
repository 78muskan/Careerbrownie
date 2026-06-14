from app.models.schemas import (
    CareerRecommendationItem,
    CareerRecommendationRequest,
    CareerRecommendationResponse,
)


CAREERS = [
    {
        "career": "AI and Machine Learning Engineer",
        "keywords": ["ai", "machine", "learning", "math", "coding", "python", "robotics"],
        "skills": ["Python", "Statistics", "Linear Algebra", "Machine Learning", "APIs"],
        "next_steps": ["Practice Python", "Build ML notebooks", "Deploy a small API"],
    },
    {
        "career": "Data Analyst",
        "keywords": ["data", "charts", "statistics", "excel", "business", "sql"],
        "skills": ["Excel", "SQL", "Python", "Statistics", "Storytelling"],
        "next_steps": ["Learn SQL", "Analyze public data", "Create dashboards"],
    },
    {
        "career": "Product Designer",
        "keywords": ["design", "creative", "apps", "drawing", "psychology", "ux"],
        "skills": ["UX Research", "Wireframing", "Visual Design", "Prototyping"],
        "next_steps": ["Study design patterns", "Create case studies", "Run user interviews"],
    },
    {
        "career": "Chartered Accountant",
        "keywords": ["commerce", "accounts", "tax", "finance", "business"],
        "skills": ["Accounting", "Taxation", "Auditing", "Business Law"],
        "next_steps": ["Plan CA foundation", "Practice accounts", "Track finance news"],
    },
]


class CareerRecommender:
    def recommend(self, payload: CareerRecommendationRequest) -> CareerRecommendationResponse:
        terms = self._tokens(
            payload.interests + payload.strengths + payload.subjects + [payload.stream or ""]
        )
        items: list[CareerRecommendationItem] = []
        for career in CAREERS:
            matches = terms.intersection(self._tokens(career["keywords"] + career["skills"]))
            score = min(99, 48 + len(matches) * 13)
            why = "Matched against interests, strengths, and subject signals"
            items.append(
                CareerRecommendationItem(
                    career=career["career"],
                    match_score=score,
                    why=why,
                    core_skills=career["skills"],
                    next_steps=career["next_steps"],
                )
            )
        items.sort(key=lambda item: item.match_score, reverse=True)
        return CareerRecommendationResponse(recommendations=items)

    def skills_for(self, target_career: str) -> list[str]:
        target_terms = self._tokens([target_career])
        best = CAREERS[0]
        best_score = 0
        for career in CAREERS:
            score = len(target_terms.intersection(self._tokens([career["career"]] + career["keywords"])))
            if score > best_score:
                best = career
                best_score = score
        return best["skills"]

    def _tokens(self, values: list[str]) -> set[str]:
        tokens: set[str] = set()
        for value in values:
            for part in str(value).replace("-", " ").replace("/", " ").split():
                clean = "".join(char for char in part.lower() if char.isalnum())
                if clean:
                    tokens.add(clean)
        return tokens
