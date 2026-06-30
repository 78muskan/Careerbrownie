from app.models.schemas import (
    CareerOption,
    CareerRecommendationRequest,
    CareerRecommendationResponse,
)


CAREERS = [
    {
        "title": "AI and Machine Learning Engineer",
        "keywords": ["ai", "machine", "learning", "math", "coding", "python", "robotics", "data"],
        "skills_to_build": ["Python", "Statistics", "Linear Algebra", "Machine Learning", "APIs"],
    },
    {
        "title": "Data Analyst",
        "keywords": ["data", "charts", "statistics", "excel", "business", "sql", "analytics"],
        "skills_to_build": ["Excel", "SQL", "Python", "Statistics", "Data Visualisation"],
    },
    {
        "title": "Product Designer (UX/UI)",
        "keywords": ["design", "creative", "apps", "drawing", "psychology", "ux", "ui", "visual"],
        "skills_to_build": ["UX Research", "Wireframing", "Figma", "Visual Design", "Prototyping"],
    },
    {
        "title": "Chartered Accountant",
        "keywords": ["commerce", "accounts", "tax", "finance", "business", "audit", "ca"],
        "skills_to_build": ["Accounting", "Taxation", "Auditing", "Business Law", "Tally"],
    },
    {
        "title": "Software Engineer",
        "keywords": ["coding", "programming", "software", "computer", "tech", "web", "app", "backend"],
        "skills_to_build": ["Data Structures", "Algorithms", "System Design", "Git", "Cloud"],
    },
    {
        "title": "Doctor (MBBS / MD)",
        "keywords": ["biology", "medicine", "doctor", "neet", "hospital", "health", "anatomy"],
        "skills_to_build": ["Biology", "Chemistry", "Clinical Skills", "Patient Communication"],
    },
    {
        "title": "Civil Services (IAS/IPS)",
        "keywords": ["upsc", "ias", "ips", "civils", "government", "administration", "public"],
        "skills_to_build": ["Current Affairs", "History", "Polity", "Essay Writing", "Interview Skills"],
    },
    {
        "title": "Management Consultant",
        "keywords": ["mba", "management", "consulting", "strategy", "business", "cat", "iim"],
        "skills_to_build": ["Problem Solving", "Business Analysis", "Communication", "Excel", "PPT"],
    },
]


class CareerRecommender:
    def recommend(self, payload: CareerRecommendationRequest) -> CareerRecommendationResponse:
        input_tokens = self._tokens(
            payload.interests
            + payload.skills
            + ([payload.academic_stream] if payload.academic_stream else [])
            + ([payload.preferred_location] if payload.preferred_location else [])
        )
        items: list[CareerOption] = []
        for career in CAREERS:
            matches = input_tokens.intersection(
                self._tokens(career["keywords"] + career["skills_to_build"])
            )
            score = round(min(99.0, 48.0 + len(matches) * 12.0), 1)
            reason = (
                f"Matched {len(matches)} signals from your interests and skills"
                if matches
                else "Broad career option worth exploring"
            )
            items.append(
                CareerOption(
                    title=career["title"],
                    match_score=score,
                    reason=reason,
                    skills_to_build=career["skills_to_build"],
                )
            )
        items.sort(key=lambda c: c.match_score, reverse=True)
        return CareerRecommendationResponse(recommendations=items)

    def skills_for(self, target_career: str) -> list[str]:
        target_tokens = self._tokens([target_career])
        best = CAREERS[0]
        best_score = 0
        for career in CAREERS:
            score = len(
                target_tokens.intersection(
                    self._tokens([career["title"]] + career["keywords"])
                )
            )
            if score > best_score:
                best = career
                best_score = score
        return best["skills_to_build"]

    def _tokens(self, values: list[str]) -> set[str]:
        tokens: set[str] = set()
        for value in values:
            for part in str(value).replace("-", " ").replace("/", " ").split():
                clean = "".join(c for c in part.lower() if c.isalnum())
                if clean:
                    tokens.add(clean)
        return tokens
