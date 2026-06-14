from app.models.schemas import (
    CollegePredictionItem,
    CollegePredictionRequest,
    CollegePredictionResponse,
)


COLLEGES = [
    {
        "college_name": "Delhi Technological University",
        "city": "Delhi",
        "state": "Delhi",
        "streams": ["science", "engineering"],
        "courses": ["B.Tech Computer Engineering", "B.Tech Data Science"],
        "min_score": 82,
        "exam": "jee",
        "fees": 220000,
    },
    {
        "college_name": "St. Xavier's College",
        "city": "Mumbai",
        "state": "Maharashtra",
        "streams": ["commerce", "arts", "science"],
        "courses": ["B.Com", "BA Psychology", "BSc Statistics"],
        "min_score": 78,
        "exam": "",
        "fees": 85000,
    },
    {
        "college_name": "Christ University",
        "city": "Bengaluru",
        "state": "Karnataka",
        "streams": ["commerce", "arts", "science"],
        "courses": ["BBA", "BSc Psychology", "BCA"],
        "min_score": 70,
        "exam": "cuet",
        "fees": 170000,
    },
]


class CollegePredictor:
    def predict(self, payload: CollegePredictionRequest) -> CollegePredictionResponse:
        locations = {location.lower() for location in payload.preferred_locations}
        exams = {exam.lower() for exam in payload.entrance_exams}
        predictions: list[CollegePredictionItem] = []
        for college in COLLEGES:
            score = 50 + payload.academic_score - college["min_score"]
            if payload.stream and payload.stream.lower() in college["streams"]:
                score += 12
            if college["city"].lower() in locations or college["state"].lower() in locations:
                score += 10
            if college["exam"] and college["exam"] in exams:
                score += 8
            if payload.budget:
                score += 5 if payload.budget >= college["fees"] else -8
            predictions.append(
                CollegePredictionItem(
                    college_name=college["college_name"],
                    city=college["city"],
                    state=college["state"],
                    fit_score=min(99, max(20, score)),
                    likely_courses=college["courses"],
                    reason="Score, stream, entrance exam, location, and budget fit were evaluated",
                )
            )
        predictions.sort(key=lambda item: item.fit_score, reverse=True)
        return CollegePredictionResponse(predictions=predictions)
