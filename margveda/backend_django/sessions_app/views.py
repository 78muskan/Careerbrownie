from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Session, CounsellorAvailability
from users.serializers import UserSerializer


class SessionSerializer(serializers.ModelSerializer):
    counsellor_name = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = [
            "id", "session_type", "status", "scheduled_at", "duration_minutes",
            "meeting_link", "notes", "student_feedback", "student_rating",
            "counsellor_name", "student_name", "is_free_session", "created_at",
        ]
        read_only_fields = ["id", "created_at", "counsellor_name", "student_name"]

    def get_counsellor_name(self, obj):
        return obj.counsellor.full_name if obj.counsellor else None

    def get_student_name(self, obj):
        return obj.student.full_name if obj.student else None


class BookSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "student":
            return Response({"error": "Only students can book sessions."}, status=status.HTTP_403_FORBIDDEN)
        data = request.data.copy()
        session_type = data.get("session_type", "career_counselling")
        scheduled_at = data.get("scheduled_at")
        if not scheduled_at:
            return Response({"error": "scheduled_at is required."}, status=status.HTTP_400_BAD_REQUEST)
        session = Session.objects.create(
            student=request.user,
            session_type=session_type,
            scheduled_at=scheduled_at,
            duration_minutes=data.get("duration_minutes", 60),
            notes=data.get("notes", ""),
            is_free_session=data.get("is_free_session", False),
        )
        from notifications.models import Notification
        Notification.create(
            user=request.user,
            notification_type="session_confirmed",
            title="Session Booked!",
            message=f"Your {session.get_session_type_display()} session on {session.scheduled_at:%d %b, %I:%M %p} has been booked.",
            link=f"/student/sessions/{session.id}",
        )
        return Response(SessionSerializer(session).data, status=status.HTTP_201_CREATED)


class StudentSessionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Session.objects.filter(student=request.user)
        session_status = request.query_params.get("status")
        if session_status:
            qs = qs.filter(status=session_status)
        return Response(SessionSerializer(qs, many=True).data)


class SessionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            s = Session.objects.get(pk=pk, student=request.user)
        except Session.DoesNotExist:
            return Response({"error": "Session not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(SessionSerializer(s).data)

    def patch(self, request, pk):
        try:
            s = Session.objects.get(pk=pk, student=request.user)
        except Session.DoesNotExist:
            return Response({"error": "Session not found."}, status=status.HTTP_404_NOT_FOUND)
        allowed = ["student_feedback", "student_rating", "status"]
        for field in allowed:
            if field in request.data:
                if field == "status" and request.data[field] not in ["cancelled_student"]:
                    continue
                setattr(s, field, request.data[field])
        s.save()
        return Response(SessionSerializer(s).data)


class CounsellorSessionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role not in ("counsellor", "admin"):
            return Response({"error": "Counsellor access only."}, status=status.HTTP_403_FORBIDDEN)
        qs = Session.objects.filter(counsellor=request.user)
        return Response(SessionSerializer(qs, many=True).data)

    def patch(self, request, pk):
        if request.user.role not in ("counsellor", "admin"):
            return Response({"error": "Counsellor access only."}, status=status.HTTP_403_FORBIDDEN)
        try:
            s = Session.objects.get(pk=pk, counsellor=request.user)
        except Session.DoesNotExist:
            return Response({"error": "Session not found."}, status=status.HTTP_404_NOT_FOUND)
        allowed = ["status", "meeting_link", "counsellor_notes"]
        for field in allowed:
            if field in request.data:
                setattr(s, field, request.data[field])
        s.save()
        if s.status == "confirmed" and s.meeting_link:
            from notifications.models import Notification
            Notification.create(
                user=s.student,
                notification_type="session_confirmed",
                title="Session Confirmed",
                message=f"Your session on {s.scheduled_at:%d %b, %I:%M %p} is confirmed. Meeting link added.",
                link=f"/student/sessions/{s.id}",
            )
        return Response(SessionSerializer(s).data)
