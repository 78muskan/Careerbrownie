from app.models.schemas import (
    CollegeOption,
    CollegePredictionRequest,
    CollegePredictionResponse,
)


COLLEGES = [
    {
        "name": "Delhi Skill and Technology University",
        "location": "Delhi",
        "streams": ["science", "technology", "engineering"],
        "courses": ["B.Tech", "Data Science", "AI Foundations"],
    },
    {
        "name": "Mumbai Commerce and Analytics College",
        "location": "Mumbai",
        "streams": ["commerce", "business", "analytics"],
        "courses": ["B.Com", "Business Analytics", "Finance"],
    },
    {
        "name": "Bengaluru Design and Innovation School",
        "location": "Bengaluru",
        "streams": ["design", "arts", "technology"],
        "courses": ["UX Design", "Product Design", "Human Computer Interaction"],
    },
]


def predict_colleges(payload: CollegePredictionRequest) -> CollegePredictionResponse:
    stream = payload.academic_stream.lower()
    preferred = (payload.preferred_location or "").lower()
    options: list[CollegeOption] = []

    for college in COLLEGES:
        stream_match = any(item in stream for item in college["streams"])
        location_match = preferred and preferred in college["location"].lower()
        score = 0.58 + (0.18 if stream_match else 0) + (0.14 if location_match else 0)
        score += min(payload.score_percent / 1000, 0.1)
        options.append(
            CollegeOption(
                name=college["name"],
                location=college["location"],
                courses=college["courses"],
                fit_score=round(min(score, 0.96), 2),
                reason="Matched using stream, score, and location preference.",
            )
        )

    options.sort(key=lambda item: item.fit_score, reverse=True)
    return CollegePredictionResponse(colleges=options)
