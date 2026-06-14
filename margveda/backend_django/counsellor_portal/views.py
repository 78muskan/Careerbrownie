from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Avg
from .models import CounsellorProfile, TimeSlot, Appointment, SessionNote, CounsellorRevenue


def is_counsellor(user):
    return user.role in ("counsellor", "admin")


# ---------------------------------------------------------------------------
# Serializers
# ---------------------------------------------------------------------------

class TimeSlotSerializer(serializers.ModelSerializer):
    weekday_name = serializers.SerializerMethodField()

    class Meta:
        model = TimeSlot
        fields = ["id", "weekday", "weekday_name", "start_time", "end_time", "duration_minutes", "is_active"]

    def get_weekday_name(self, obj):
        return obj.get_weekday_display()


class AppointmentSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    counsellor_name = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ["id", "scheduled_date", "start_time", "end_time", "duration_minutes",
                  "status", "session_type", "meeting_link", "student_notes",
                  "is_free", "student_name", "counsellor_name", "created_at"]

    def get_student_name(self, obj):
        return obj.student.full_name if obj.student else None

    def get_counsellor_name(self, obj):
        return obj.counsellor.full_name if obj.counsellor else None


class SessionNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionNote
        fields = ["id", "key_points", "action_items", "resources_shared",
                  "student_feedback", "student_rating", "next_session_notes",
                  "is_private", "created_at", "updated_at"]


class CounsellorProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    user_avatar = serializers.SerializerMethodField()

    class Meta:
        model = CounsellorProfile
        fields = ["id", "user_email", "user_name", "user_avatar", "bio", "tagline",
                  "experience_years", "specializations", "education", "certifications",
                  "languages", "hourly_rate", "free_session_minutes", "linkedin_url",
                  "total_sessions_conducted", "total_students_guided", "avg_rating",
                  "is_accepting_students", "is_verified"]
        read_only_fields = ["id", "total_sessions_conducted", "total_students_guided",
                            "avg_rating", "is_verified", "user_email", "user_name", "user_avatar"]

    def get_user_email(self, obj): return obj.user.email
    def get_user_name(self, obj): return obj.user.full_name
    def get_user_avatar(self, obj):
        req = self.context.get("request")
        if obj.user.avatar and req:
            return req.build_absolute_uri(obj.user.avatar.url)
        return None


# ---------------------------------------------------------------------------
# Counsellor Profile
# ---------------------------------------------------------------------------

class CounsellorProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not is_counsellor(request.user):
            return Response({"error": "Counsellor access only."}, status=status.HTTP_403_FORBIDDEN)
        profile, _ = CounsellorProfile.objects.get_or_create(user=request.user)
        return Response(CounsellorProfileSerializer(profile, context={"request": request}).data)

    def patch(self, request):
        if not is_counsellor(request.user):
            return Response({"error": "Counsellor access only."}, status=status.HTTP_403_FORBIDDEN)
        profile, _ = CounsellorProfile.objects.get_or_create(user=request.user)
        serializer = CounsellorProfileSerializer(profile, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicCounsellorListView(APIView):
    def get(self, request):
        profiles = CounsellorProfile.objects.filter(is_accepting_students=True, is_verified=True).select_related("user")
        return Response(CounsellorProfileSerializer(profiles, many=True, context={"request": request}).data)


class PublicCounsellorDetailView(APIView):
    def get(self, request, pk):
        try:
            profile = CounsellorProfile.objects.select_related("user").get(pk=pk, is_accepting_students=True)
        except CounsellorProfile.DoesNotExist:
            return Response({"error": "Counsellor not found."}, status=status.HTTP_404_NOT_FOUND)
        slots = TimeSlot.objects.filter(counsellor=profile.user, is_active=True)
        data = CounsellorProfileSerializer(profile, context={"request": request}).data
        data["available_slots"] = TimeSlotSerializer(slots, many=True).data
        return Response(data)


# ---------------------------------------------------------------------------
# Availability / Time Slots
# ---------------------------------------------------------------------------

class TimeSlotView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not is_counsellor(request.user):
            return Response({"error": "Counsellor access only."}, status=status.HTTP_403_FORBIDDEN)
        slots = TimeSlot.objects.filter(counsellor=request.user)
        return Response(TimeSlotSerializer(slots, many=True).data)

    def post(self, request):
        if not is_counsellor(request.user):
            return Response({"error": "Counsellor access only."}, status=status.HTTP_403_FORBIDDEN)
        serializer = TimeSlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(counsellor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TimeSlotDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            slot = TimeSlot.objects.get(pk=pk, counsellor=request.user)
        except TimeSlot.DoesNotExist:
            return Response({"error": "Slot not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = TimeSlotSerializer(slot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            TimeSlot.objects.get(pk=pk, counsellor=request.user).delete()
        except TimeSlot.DoesNotExist:
            return Response({"error": "Slot not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------------------------------------------------------------------
# Appointments / Booking
# ---------------------------------------------------------------------------

class BookAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "student":
            return Response({"error": "Students only."}, status=status.HTTP_403_FORBIDDEN)
        counsellor_id = request.data.get("counsellor_id")
        scheduled_date = request.data.get("scheduled_date")
        start_time = request.data.get("start_time")
        if not all([counsellor_id, scheduled_date, start_time]):
            return Response({"error": "counsellor_id, scheduled_date, start_time are required."},
                status=status.HTTP_400_BAD_REQUEST)
        # Check no double-booking
        if Appointment.objects.filter(counsellor_id=counsellor_id, scheduled_date=scheduled_date,
                start_time=start_time, status__in=["requested", "confirmed"]).exists():
            return Response({"error": "This slot is already booked."}, status=status.HTTP_409_CONFLICT)
        appt = Appointment.objects.create(
            counsellor_id=counsellor_id,
            student=request.user,
            scheduled_date=scheduled_date,
            start_time=start_time,
            end_time=request.data.get("end_time", start_time),
            duration_minutes=request.data.get("duration_minutes", 60),
            session_type=request.data.get("session_type", "career_counselling"),
            student_notes=request.data.get("notes", ""),
            is_free=request.data.get("is_free", False),
            status="requested",
        )
        from notifications.models import Notification
        Notification.create(user=request.user, notification_type="session_confirmed",
            title="Appointment Requested!",
            message=f"Your appointment on {appt.scheduled_date} at {appt.start_time} has been requested.",
            link=f"/student/sessions/{appt.id}")
        return Response(AppointmentSerializer(appt).data, status=status.HTTP_201_CREATED)


class CounsellorCalendarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not is_counsellor(request.user):
            return Response({"error": "Counsellor access only."}, status=status.HTTP_403_FORBIDDEN)
        from_date = request.query_params.get("from")
        to_date = request.query_params.get("to")
        qs = Appointment.objects.filter(counsellor=request.user)
        if from_date:
            qs = qs.filter(scheduled_date__gte=from_date)
        if to_date:
            qs = qs.filter(scheduled_date__lte=to_date)
        return Response(AppointmentSerializer(qs, many=True).data)


class AppointmentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            if is_counsellor(request.user):
                appt = Appointment.objects.get(pk=pk, counsellor=request.user)
            else:
                appt = Appointment.objects.get(pk=pk, student=request.user)
        except Appointment.DoesNotExist:
            return Response({"error": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        data = AppointmentSerializer(appt).data
        try:
            data["session_note"] = SessionNoteSerializer(appt.session_note).data
        except SessionNote.DoesNotExist:
            data["session_note"] = None
        return Response(data)

    def patch(self, request, pk):
        try:
            if is_counsellor(request.user):
                appt = Appointment.objects.get(pk=pk, counsellor=request.user)
            else:
                return Response({"error": "Counsellor access only."}, status=status.HTTP_403_FORBIDDEN)
        except Appointment.DoesNotExist:
            return Response({"error": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        for field in ["status", "meeting_link"]:
            if field in request.data:
                setattr(appt, field, request.data[field])
        appt.save()
        if appt.status == "confirmed" and appt.student:
            from notifications.models import Notification
            Notification.create(user=appt.student, notification_type="session_confirmed",
                title="Appointment Confirmed!",
                message=f"Your session on {appt.scheduled_date} is confirmed.",
                link=f"/student/sessions/{appt.id}")
            # Auto-create revenue record
            try:
                cp = appt.counsellor.counsellor_profile
                amount = float(cp.hourly_rate) * (appt.duration_minutes / 60)
                platform_fee = round(amount * 0.15, 2)
                CounsellorRevenue.objects.get_or_create(
                    counsellor=appt.counsellor, appointment=appt,
                    defaults={"amount": amount, "platform_fee": platform_fee}
                )
            except Exception:
                pass
        return Response(AppointmentSerializer(appt).data)


# ---------------------------------------------------------------------------
# Session Notes
# ---------------------------------------------------------------------------

class SessionNoteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, appointment_id):
        try:
            appt = Appointment.objects.get(pk=appointment_id, counsellor=request.user)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)
        try:
            return Response(SessionNoteSerializer(appt.session_note).data)
        except SessionNote.DoesNotExist:
            return Response({"exists": False})

    def post(self, request, appointment_id):
        if not is_counsellor(request.user):
            return Response({"error": "Counsellor access only."}, status=status.HTTP_403_FORBIDDEN)
        try:
            appt = Appointment.objects.get(pk=appointment_id, counsellor=request.user)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = SessionNoteSerializer(data=request.data)
        if serializer.is_valid():
            note, _ = SessionNote.objects.update_or_create(
                appointment=appt, defaults={**serializer.validated_data, "counsellor": request.user}
            )
            return Response(SessionNoteSerializer(note).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------------
# Reports & Revenue
# ---------------------------------------------------------------------------

class CounsellorReportsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not is_counsellor(request.user):
            return Response({"error": "Counsellor access only."}, status=status.HTTP_403_FORBIDDEN)
        appts = Appointment.objects.filter(counsellor=request.user)
        revenue_qs = CounsellorRevenue.objects.filter(counsellor=request.user)
        total_revenue = revenue_qs.aggregate(s=Sum("net_amount"))["s"] or 0
        pending_revenue = revenue_qs.filter(payment_status="pending").aggregate(s=Sum("net_amount"))["s"] or 0
        avg_rating_val = appts.filter(session_note__student_rating__isnull=False).aggregate(
            avg=Avg("session_note__student_rating"))["avg"] or 0
        monthly = list(
            appts.filter(status="completed").extra(select={"month": "strftime('%Y-%m', scheduled_date)"})
            .values("month").annotate(count=Count("id")).order_by("month")
        )
        return Response({
            "summary": {
                "total_sessions": appts.count(),
                "completed_sessions": appts.filter(status="completed").count(),
                "upcoming_sessions": appts.filter(status__in=["requested", "confirmed"]).count(),
                "total_revenue": float(total_revenue),
                "pending_revenue": float(pending_revenue),
                "avg_rating": round(float(avg_rating_val), 2),
                "unique_students": appts.filter(student__isnull=False).values("student").distinct().count(),
            },
            "monthly_sessions": monthly,
            "recent_appointments": AppointmentSerializer(appts.order_by("-created_at")[:5], many=True).data,
        })
