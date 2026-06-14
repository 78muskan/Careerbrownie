from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import PredictorResult
from universities.data import EXAM_CUTOFFS


def predict_colleges(exam_type: str, score: float, category: str) -> list:
    """Return list of colleges the student likely qualifies for."""
    cutoff_data = EXAM_CUTOFFS.get(exam_type)
    if not cutoff_data:
        return []

    results = []
    cutoffs_key = "cutoff_by_rank" if "rank" in cutoff_data else "cutoff_by_percentile"
    if "score" in cutoff_data:
        cutoffs_key = "cutoff_by_score"

    cutoffs = cutoff_data.get(cutoffs_key, {})
    is_rank_based = cutoffs_key == "cutoff_by_rank"

    for college, cat_cutoffs in cutoffs.items():
        threshold = cat_cutoffs.get(category, cat_cutoffs.get("general"))
        if threshold is None:
            continue

        if is_rank_based:
            # Lower rank = better; qualify if student's rank <= threshold
            qualifies = score <= threshold
            margin = threshold - score
        else:
            # Higher score/percentile = better
            qualifies = score >= threshold
            margin = score - threshold

        if qualifies or (not is_rank_based and margin >= -10) or (is_rank_based and margin >= -200):
            results.append({
                "college": college,
                "cutoff": threshold,
                "student_score": score,
                "qualifies": qualifies,
                "margin": round(abs(margin), 2),
                "admission_chance": "High" if (not is_rank_based and margin >= 5) or (is_rank_based and margin >= 100)
                                    else "Moderate" if qualifies
                                    else "Low",
            })

    results.sort(key=lambda x: (0 if x["qualifies"] else 1, -x["margin"] if not is_rank_based else x["margin"]))
    return results


class CollegePredictorView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        exam_type = request.data.get("exam_type")
        score = request.data.get("score")
        category = request.data.get("category", "general")

        if not exam_type or score is None:
            return Response({"error": "exam_type and score are required."}, status=400)

        try:
            score = float(score)
        except (TypeError, ValueError):
            return Response({"error": "score must be a number."}, status=400)

        if exam_type not in EXAM_CUTOFFS:
            return Response({
                "error": f"Invalid exam_type. Choose from: {', '.join(EXAM_CUTOFFS.keys())}"
            }, status=400)

        predicted = predict_colleges(exam_type, score, category)

        result = PredictorResult.objects.create(
            student=request.user if request.user.is_authenticated else None,
            exam_type=exam_type,
            score=score,
            category=category,
            predicted_colleges=predicted,
        )

        return Response({
            "id": str(result.id),
            "exam_type": exam_type,
            "score": score,
            "category": category,
            "predicted_colleges": predicted,
            "total_matches": len(predicted),
        }, status=status.HTTP_201_CREATED)


class SupportedExamsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        exams = []
        for exam_key, data in EXAM_CUTOFFS.items():
            exams.append({
                "key": exam_key,
                "name": data["exam_name"],
                "for_admission_to": data["for_admission_to"],
                "note": data.get("note", ""),
            })
        return Response(exams)


class MyPredictionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        results = PredictorResult.objects.filter(student=request.user)[:10]
        data = [
            {
                "id": str(r.id),
                "exam_type": r.exam_type,
                "score": r.score,
                "category": r.category,
                "total_matches": len(r.predicted_colleges),
                "created_at": r.created_at,
            }
            for r in results
        ]
        return Response(data)
