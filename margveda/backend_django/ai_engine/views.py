from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import AssessmentResult, CareerRoadmap, AIInsight
from .scoring import (
    score_interest_assessment, score_personality_assessment,
    score_aptitude_assessment, score_readiness_assessment,
    match_careers, generate_skill_gaps, get_market_trends, calculate_career_score,
)
from .career_data import (
    INTEREST_QUESTIONS, PERSONALITY_QUESTIONS, APTITUDE_QUESTIONS,
    READINESS_QUESTIONS, CAREERS, ROADMAP_TEMPLATES, LEARNING_RESOURCES,
)


def _get_profile(user):
    try:
        return user.student_profile
    except Exception:
        return None


class AssessmentQuestionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, assessment_type):
        MAP = {
            "interest": INTEREST_QUESTIONS,
            "personality": PERSONALITY_QUESTIONS,
            "aptitude": APTITUDE_QUESTIONS,
            "readiness": READINESS_QUESTIONS,
        }
        if assessment_type not in MAP:
            return Response({"error": "Invalid assessment type."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"questions": MAP[assessment_type], "assessment_type": assessment_type})


class SubmitAssessmentView(APIView):
    permission_classes = [IsAuthenticated]

    SCORERS = {
        "interest": score_interest_assessment,
        "personality": score_personality_assessment,
        "aptitude": score_aptitude_assessment,
        "readiness": score_readiness_assessment,
    }

    def post(self, request, assessment_type):
        if assessment_type not in self.SCORERS:
            return Response({"error": "Invalid assessment type."}, status=status.HTTP_400_BAD_REQUEST)
        profile = _get_profile(request.user)
        if not profile:
            return Response({"error": "Student profile required."}, status=status.HTTP_403_FORBIDDEN)
        responses = request.data.get("responses", {})
        scores = self.SCORERS[assessment_type](responses)
        top_careers = []
        if assessment_type == "interest":
            top_careers = match_careers(scores.get("top_codes", []), profile.technical_skills or [], profile.career_interests or [])
        summary = self._build_summary(assessment_type, scores)
        result, _ = AssessmentResult.objects.update_or_create(
            student=profile, assessment_type=assessment_type,
            defaults={"responses": responses, "scores": scores, "result_summary": summary, "top_careers": top_careers},
        )
        if hasattr(profile, "career_profile"):
            cp = profile.career_profile
            if assessment_type == "interest" and top_careers:
                cp.ai_career_recommendations = [c["title"] for c in top_careers[:5]]
            if assessment_type == "personality":
                cp.personality_type = scores.get("archetype", "")
            cp.assessment_completed = profile.assessment_results.count() >= 2
            cp.career_score = calculate_career_score(profile)
            cp.save()
        self._generate_insights(profile, assessment_type, scores, top_careers)
        from notifications.models import Notification
        Notification.create(user=request.user, notification_type="ai_insight",
            title=f"{assessment_type.replace('_', ' ').title()} Assessment Complete!",
            message="Your results are ready. Check your AI career insights.", link="/student/ai-advisor")
        return Response({"result": {"id": str(result.id), "assessment_type": assessment_type,
            "scores": scores, "result_summary": summary, "top_careers": top_careers}}, status=status.HTTP_201_CREATED)

    def _build_summary(self, assessment_type, scores):
        if assessment_type == "interest":
            primary = scores.get("primary", "I")
            names = {"R": "Realistic", "I": "Investigative", "A": "Artistic", "S": "Social", "E": "Enterprising", "C": "Conventional"}
            return f"Your primary interest type is {names.get(primary, primary)}. You thrive in environments that reward logical thinking and discovery."
        elif assessment_type == "personality":
            return f"Personality archetype: {scores.get('archetype', 'Balanced Achiever')}. You bring structured thinking and collaborative energy to your work."
        elif assessment_type == "aptitude":
            total = scores.get("scores", {}).get("total", 0)
            strengths = scores.get("strengths", [])
            return f"Aptitude score: {total}%. Strengths: {', '.join(strengths) or 'general reasoning'}."
        elif assessment_type == "readiness":
            level, overall = scores.get("level", "Developing"), scores.get("overall", 0)
            return f"Career Readiness: {level} ({overall}%). Strengthen your weaker areas to accelerate your journey."
        return ""

    def _generate_insights(self, profile, assessment_type, scores, top_careers):
        if assessment_type == "interest" and top_careers:
            AIInsight.objects.update_or_create(student=profile, insight_type="career_match", defaults={
                "title": f"Top Career Match: {top_careers[0]['title']}",
                "content": f"You have a {top_careers[0]['match_pct']}% match with {top_careers[0]['title']} based on your interests.",
                "data": {"careers": top_careers[:3]}, "relevance_score": top_careers[0]["match_pct"] / 100,
            })
        gaps = generate_skill_gaps(
            (profile.target_roles or [])[0].lower().replace(" ", "_") if profile.target_roles else "software_engineer",
            profile.technical_skills or [],
        )
        if gaps:
            AIInsight.objects.update_or_create(student=profile, insight_type="skill_gap", defaults={
                "title": "Key skills to develop", "content": f"Focus on: {', '.join(gaps)}.",
                "data": {"gaps": gaps}, "relevance_score": 0.8,
            })


class AssessmentResultView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, assessment_type=None):
        profile = _get_profile(request.user)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        if assessment_type:
            try:
                r = AssessmentResult.objects.get(student=profile, assessment_type=assessment_type)
                return Response({"assessment_type": r.assessment_type, "scores": r.scores,
                    "result_summary": r.result_summary, "top_careers": r.top_careers, "completed_at": r.completed_at})
            except AssessmentResult.DoesNotExist:
                return Response({"error": "Not taken yet."}, status=status.HTTP_404_NOT_FOUND)
        results = AssessmentResult.objects.filter(student=profile)
        return Response([{"assessment_type": r.assessment_type, "result_summary": r.result_summary,
            "completed_at": r.completed_at} for r in results])


class RoadmapView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = _get_profile(request.user)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        try:
            return Response(self._serialize(profile.roadmap))
        except CareerRoadmap.DoesNotExist:
            return Response({"exists": False}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        profile = _get_profile(request.user)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_403_FORBIDDEN)
        target = request.data.get("target_career", "").lower().replace(" ", "_")
        key = target if target in ROADMAP_TEMPLATES else "default"
        t = ROADMAP_TEMPLATES[key]
        roadmap, _ = CareerRoadmap.objects.update_or_create(student=profile, defaults={
            "target_career": request.data.get("target_career", "Career Path"),
            "plan_3_months": t["3_months"], "plan_6_months": t["6_months"],
            "plan_1_year": t["1_year"], "plan_3_years": t["3_years"], "plan_5_years": t["5_years"],
        })
        return Response(self._serialize(roadmap), status=status.HTTP_201_CREATED)

    def _serialize(self, rm):
        return {"id": str(rm.id), "target_career": rm.target_career, "generated_at": rm.generated_at,
            "plans": {"3_months": rm.plan_3_months, "6_months": rm.plan_6_months,
                "1_year": rm.plan_1_year, "3_years": rm.plan_3_years, "5_years": rm.plan_5_years}}


class AIAdvisorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = _get_profile(request.user)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        insights = AIInsight.objects.filter(student=profile)
        skill_gaps = generate_skill_gaps(
            (profile.target_roles or [])[0].lower().replace(" ", "_") if profile.target_roles else "software_engineer",
            profile.technical_skills or [],
        )
        trends = get_market_trends(profile.career_interests or [])
        career_matches = match_careers(["I", "E", "A"], profile.technical_skills or [], profile.career_interests or [])
        resources = []
        for gap in skill_gaps[:3]:
            for sname, res_list in LEARNING_RESOURCES.items():
                if sname.lower() in gap.lower():
                    resources.extend(res_list[:2])
                    break
        return Response({
            "insights": [{"type": i.insight_type, "title": i.title, "content": i.content, "data": i.data} for i in insights[:8]],
            "career_matches": career_matches[:6],
            "skill_gaps": skill_gaps,
            "market_trends": trends,
            "learning_resources": resources[:6],
            "assessments_completed": list(profile.assessment_results.values_list("assessment_type", flat=True)),
        })


class CareerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, career_key):
        career = CAREERS.get(career_key)
        if not career:
            return Response({"error": "Career not found."}, status=status.HTTP_404_NOT_FOUND)
        profile = _get_profile(request.user)
        skill_gaps = generate_skill_gaps(career_key, profile.technical_skills if profile else [])
        resources = [r for skill in career["key_skills"][:3]
            for sname, res_list in LEARNING_RESOURCES.items()
            if sname.lower() in skill.lower() for r in res_list[:2]]
        return Response({**career, "key": career_key, "skill_gaps": skill_gaps, "learning_resources": resources[:5]})


class CareerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        domain = request.query_params.get("domain")
        return Response([
            {"key": k, "title": v["title"], "domain": v["domain"],
             "avg_salary_india": v["avg_salary_india"], "demand": v["demand"], "growth_rate": v["growth_rate"]}
            for k, v in CAREERS.items() if not domain or v["domain"].lower() == domain.lower()
        ])
