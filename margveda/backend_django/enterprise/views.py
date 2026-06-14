from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (EnterpriseClient, AICareerTwinSession,
                     AIVideoInterviewQuestion, AIPlacementPrediction)
from students.models import CareerProfile
from ai_engine.models import AssessmentResult, CareerRoadmap
from ai_engine.scoring import match_careers, generate_skill_gaps, calculate_career_score


class EnterpriseClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnterpriseClient
        fields = ["id", "name", "client_type", "contact_name", "contact_email",
                  "city", "state", "license_type", "license_expiry", "max_users",
                  "current_users", "contract_value", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]


class AICareerTwinSerializer(serializers.ModelSerializer):
    class Meta:
        model = AICareerTwinSession
        fields = ["id", "recommendations", "action_plan", "predicted_placement_score",
                  "predicted_career_fit", "career_profile_snapshot", "session_context", "created_at"]
        read_only_fields = fields


class VideoQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIVideoInterviewQuestion
        fields = ["id", "question_text", "category", "difficulty", "time_limit_seconds", "tips"]


class PlacementPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIPlacementPrediction
        fields = ["id", "placement_probability", "predicted_package_min", "predicted_package_max",
                  "top_matching_companies", "skill_gap_impact", "timeline_to_ready", "created_at"]
        read_only_fields = fields


# ---------- Enterprise Client Admin ----------

class EnterpriseClientListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response(EnterpriseClientSerializer(EnterpriseClient.objects.all(), many=True).data)

    def post(self, request):
        serializer = EnterpriseClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = serializer.save()
        return Response(EnterpriseClientSerializer(client).data, status=status.HTTP_201_CREATED)


class EnterpriseClientDetailView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        client = get_object_or_404(EnterpriseClient, pk=pk)
        serializer = EnterpriseClientSerializer(client, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# ---------- AI Career Twin ----------

def _build_twin_data(student):
    try:
        cp = CareerProfile.objects.get(student=student)
    except CareerProfile.DoesNotExist:
        return None

    assessments = {a.assessment_type: a.scores
                   for a in AssessmentResult.objects.filter(student=student)}

    riasec_codes = assessments.get("interest", {}).get("top_codes", [])
    career_matches = match_careers(riasec_codes, cp.skills or [], cp.career_interests or [])
    predicted_career = (career_matches[0]["career_key"] if career_matches
                        else (cp.top_careers or ["software_engineer"])[0])
    skill_gaps = generate_skill_gaps(predicted_career, cp.skills or [])
    career_score = calculate_career_score(cp)

    recommendations = []
    if skill_gaps:
        recommendations.append({
            "type": "skill", "priority": "high",
            "title": f"Learn {skill_gaps[0]}",
            "description": f"Top missing skill for {predicted_career.replace('_', ' ').title()}",
        })
    if len(assessments) < 4:
        recommendations.append({
            "type": "assessment", "priority": "medium",
            "title": "Complete all 4 assessments",
            "description": "Unlock full AI accuracy by completing remaining assessments",
        })
    if career_score < 60:
        recommendations.append({
            "type": "profile", "priority": "medium",
            "title": "Improve career profile",
            "description": "Add more goals and interests to boost your AI match accuracy",
        })
    if not CareerRoadmap.objects.filter(student=student).exists():
        recommendations.append({
            "type": "roadmap", "priority": "low",
            "title": "Generate your career roadmap",
            "description": "Get a personalised 5-year plan for your target career",
        })

    action_plan = [
        {"week": 1, "task": f"Build skill: {skill_gaps[0]}" if skill_gaps else "Explore career options"},
        {"week": 2, "task": "Build a project showcasing your best skill"},
        {"week": 4, "task": "Update resume with latest projects and achievements"},
        {"week": 8, "task": "Apply to 5 internships or entry-level roles"},
        {"week": 12, "task": "Book a counsellor session for personalised guidance"},
    ]

    placement_score = min(career_score // 2 + len(assessments) * 10 + (20 if not skill_gaps else 0), 100)

    return {
        "session_context": {
            "career_score": career_score,
            "assessments_done": list(assessments.keys()),
            "top_career_match": predicted_career,
            "skill_gaps": skill_gaps[:5],
        },
        "career_profile_snapshot": {
            "skills": (cp.skills or [])[:10],
            "interests": cp.career_interests or [],
            "top_careers": cp.top_careers or [],
        },
        "recommendations": recommendations,
        "action_plan": action_plan,
        "predicted_placement_score": placement_score,
        "predicted_career_fit": predicted_career.replace("_", " ").title(),
    }


class AICareerTwinView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        latest = AICareerTwinSession.objects.filter(student=request.user).first()
        if latest:
            return Response(AICareerTwinSerializer(latest).data)
        return self.post(request)

    def post(self, request):
        data = _build_twin_data(request.user)
        if not data:
            return Response({"error": "Complete your profile first to activate AI Career Twin"}, status=400)
        session = AICareerTwinSession.objects.create(student=request.user, **data)
        return Response(AICareerTwinSerializer(session).data, status=status.HTTP_201_CREATED)


# ---------- AI Video Interviewer ----------

class VideoInterviewQuestionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = AIVideoInterviewQuestion.objects.filter(is_active=True)
        category = request.query_params.get("category")
        difficulty = request.query_params.get("difficulty")
        if category:
            qs = qs.filter(category=category)
        if difficulty:
            qs = qs.filter(difficulty=difficulty)
        return Response(VideoQuestionSerializer(qs[:10], many=True).data)


# ---------- AI Placement Predictor ----------

def _predict_placement(student):
    try:
        cp = CareerProfile.objects.get(student=student)
    except CareerProfile.DoesNotExist:
        return None

    assessments_done = AssessmentResult.objects.filter(student=student).count()
    skills_count = len(cp.skills or [])
    career_score = calculate_career_score(cp)

    probability = round(min(
        career_score * 0.3 / 100 +
        assessments_done * 0.1 +
        min(skills_count * 0.03, 0.3),
        0.98
    ), 2)

    predicted_min = 300000 + round(probability * 700000)
    predicted_max = predicted_min + 200000

    domain_companies = {
        "technology": ["Infosys", "TCS", "Wipro", "HCL", "Tech Mahindra"],
        "finance": ["HDFC Bank", "ICICI Bank", "Axis Bank", "Deloitte", "EY"],
        "marketing": ["WPP", "Publicis", "Ogilvy", "GroupM", "MindShare"],
        "data_science": ["Mu Sigma", "Fractal", "LatentView", "Accenture", "Tiger Analytics"],
    }
    companies = domain_companies.get(cp.career_domain or "technology",
                                     domain_companies["technology"])

    skill_gap_impact = {}
    if cp.top_careers:
        for gap in generate_skill_gaps(cp.top_careers[0], cp.skills or [])[:3]:
            skill_gap_impact[gap] = "Adding this skill could increase placement probability by 5–10%"

    return {
        "placement_probability": probability,
        "predicted_package_min": predicted_min,
        "predicted_package_max": predicted_max,
        "top_matching_companies": companies[:max(round(probability * 5), 1)],
        "skill_gap_impact": skill_gap_impact,
        "timeline_to_ready": max(12 - round(probability * 10), 1),
        "model_inputs": {
            "career_score": career_score,
            "assessments_completed": assessments_done,
            "skills_count": skills_count,
        },
    }


class PlacementPredictorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        latest = AIPlacementPrediction.objects.filter(student=request.user).first()
        if latest:
            return Response(PlacementPredictionSerializer(latest).data)
        return self.post(request)

    def post(self, request):
        data = _predict_placement(request.user)
        if not data:
            return Response({"error": "Complete your profile to get placement prediction"}, status=400)
        prediction = AIPlacementPrediction.objects.create(student=request.user, **data)
        return Response(PlacementPredictionSerializer(prediction).data, status=status.HTTP_201_CREATED)


# ---------- Enterprise Admin Stats ----------

class EnterpriseStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        from users.models import User
        from recruiter_portal.models import JobApplication
        from school_portal.models import School

        return Response({
            "total_students": User.objects.filter(role="student").count(),
            "total_counsellors": User.objects.filter(role="counsellor").count(),
            "total_schools": School.objects.filter(is_active=True).count(),
            "total_enterprises": EnterpriseClient.objects.filter(is_active=True).count(),
            "total_job_applications": JobApplication.objects.count(),
            "assessments_completed": AssessmentResult.objects.count(),
        })
