from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import StudentProfile, CareerProfile, Goal


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ["id", "title", "description", "target_date", "status", "is_ai_suggested", "created_at"]
        read_only_fields = ["id", "created_at"]


class CareerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerProfile
        fields = [
            "career_score", "ai_career_recommendations", "skill_gaps",
            "recommended_courses", "career_roadmap", "personality_type",
            "assessment_completed", "last_ai_analysis",
        ]
        read_only_fields = ["career_score", "last_ai_analysis"]


class StudentProfileSerializer(serializers.ModelSerializer):
    career_profile = CareerProfileSerializer(read_only=True)
    goals = GoalSerializer(many=True, read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            "id", "current_education", "stream", "institution_name",
            "graduation_year", "percentage_cgpa", "city", "state",
            "career_interests", "preferred_industries", "target_roles",
            "technical_skills", "soft_skills", "certifications", "languages",
            "short_term_goal", "long_term_goal", "preferred_work_style",
            "salary_expectation", "study_abroad_interest",
            "profile_score", "onboarding_completed",
            "career_profile", "goals",
        ]


class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.student_profile
        except StudentProfile.DoesNotExist:
            return Response({"error": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(StudentProfileSerializer(profile).data)

    def patch(self, request):
        try:
            profile = request.user.student_profile
        except StudentProfile.DoesNotExist:
            return Response({"error": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            profile.calculate_score()
            if profile.profile_score >= 80 and not profile.onboarding_completed:
                profile.onboarding_completed = True
                profile.save(update_fields=["onboarding_completed"])
            from notifications.models import AuditLog
            AuditLog.objects.create(user=request.user, action="profile_update")
            return Response(StudentProfileSerializer(profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "student":
            return Response({"error": "Student access only."}, status=status.HTTP_403_FORBIDDEN)
        try:
            profile = request.user.student_profile
        except StudentProfile.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        from sessions_app.models import Session
        upcoming = Session.objects.filter(
            student=request.user, status__in=["pending", "confirmed"]
        ).order_by("scheduled_at")[:3]

        past = Session.objects.filter(
            student=request.user, status="completed"
        ).order_by("-scheduled_at")[:3]

        from notifications.models import Notification
        notifications = Notification.objects.filter(
            user=request.user, is_read=False
        ).order_by("-created_at")[:5]

        career_recs = []
        skill_gaps = []
        if hasattr(profile, "career_profile"):
            career_recs = profile.career_profile.ai_career_recommendations[:5]
            skill_gaps = profile.career_profile.skill_gaps[:4]

        def session_data(s):
            return {
                "id": str(s.id),
                "type": s.get_session_type_display(),
                "status": s.status,
                "scheduled_at": s.scheduled_at.isoformat(),
                "counsellor": s.counsellor.full_name if s.counsellor else None,
                "duration_minutes": s.duration_minutes,
                "meeting_link": s.meeting_link,
            }

        return Response({
            "profile": {
                "full_name": request.user.full_name,
                "avatar": request.build_absolute_uri(request.user.avatar.url) if request.user.avatar else None,
                "is_verified": request.user.is_verified,
                "profile_score": profile.profile_score,
                "onboarding_completed": profile.onboarding_completed,
                "career_score": profile.career_profile.career_score if hasattr(profile, "career_profile") else 0,
            },
            "career_recommendations": career_recs,
            "skill_gaps": skill_gaps,
            "upcoming_sessions": [session_data(s) for s in upcoming],
            "past_sessions": [session_data(s) for s in past],
            "total_sessions": Session.objects.filter(student=request.user).count(),
            "unread_notifications": notifications.count(),
            "goals": GoalSerializer(
                profile.goals.filter(status__in=["pending", "in_progress"])[:5], many=True
            ).data,
        })


class GoalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.student_profile
        return Response(GoalSerializer(profile.goals.all(), many=True).data)

    def post(self, request):
        profile = request.user.student_profile
        serializer = GoalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoalDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            goal = Goal.objects.get(pk=pk, student=request.user.student_profile)
        except Goal.DoesNotExist:
            return Response({"error": "Goal not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = GoalSerializer(goal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            goal = Goal.objects.get(pk=pk, student=request.user.student_profile)
        except Goal.DoesNotExist:
            return Response({"error": "Goal not found."}, status=status.HTTP_404_NOT_FOUND)
        goal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
