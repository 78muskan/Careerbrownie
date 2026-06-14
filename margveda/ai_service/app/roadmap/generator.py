from app.models.schemas import RoadmapRequest, RoadmapResponse, RoadmapStage


def generate_roadmap(payload: RoadmapRequest) -> RoadmapResponse:
    goal = payload.career_goal
    months = payload.timeline_months

    return RoadmapResponse(
        title=f"{goal} Learning Roadmap",
        career_goal=goal,
        stages=[
            RoadmapStage(
                title="Explore and Assess",
                description=f"Understand {goal}, daily responsibilities, exams, degree paths, and career outcomes.",
                duration="2 weeks",
                resources=["Career interviews", "Intro articles", "Aptitude reflection"],
            ),
            RoadmapStage(
                title="Build Foundations",
                description="Study the core subjects and tools needed for the chosen career.",
                duration=f"{max(1, months // 4)} months",
                resources=["Beginner course", "Practice notebook", "Weekly mentor review"],
            ),
            RoadmapStage(
                title="Create Proof of Work",
                description="Complete projects, case studies, volunteering, internships, or exam practice.",
                duration=f"{max(1, months // 3)} months",
                resources=["Portfolio", "Mock tests", "Feedback sessions"],
            ),
            RoadmapStage(
                title="Apply and Improve",
                description="Prepare applications, interviews, college shortlists, and a backup plan.",
                duration=f"{max(1, months // 4)} months",
                resources=["Resume", "College list", "Mock interview"],
            ),
        ],
    )
