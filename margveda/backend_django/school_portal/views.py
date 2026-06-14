from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from .models import School, StudentBatch, BatchStudent, ParentProfile, SchoolReport
from students.models import CareerProfile
from ai_engine.models import AssessmentResult


class IsSchoolAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and hasattr(request.user, "school_admin_profile")


def _get_school(user):
    return user.school_admin_profile.school


class SchoolSerializer(serializers.ModelSerializer):
    batch_count = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = ["id", "name", "code", "school_type", "city", "state",
                  "subscription_plan", "max_students", "is_active", "joined_at",
                  "batch_count", "student_count"]

    def get_batch_count(self, obj):
        return obj.batches.filter(is_active=True).count()

    def get_student_count(self, obj):
        return BatchStudent.objects.filter(batch__school=obj).values("student").distinct().count()


class BatchSerializer(serializers.ModelSerializer):
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = StudentBatch
        fields = ["id", "name", "grade", "academic_year", "class_teacher",
                  "is_active", "student_count", "created_at"]

    def get_student_count(self, obj):
        return obj.students.count()


class BatchStudentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    student_email = serializers.CharField(source="student.email", read_only=True)

    class Meta:
        model = BatchStudent
        fields = ["id", "student", "student_name", "student_email", "roll_number", "joined_at"]
        read_only_fields = ["id", "joined_at"]


class ParentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentProfile
        fields = ["id", "parent_name", "email", "phone", "relationship",
                  "occupation", "is_portal_enabled"]
        read_only_fields = ["id"]


class SchoolReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolReport
        fields = ["id", "report_type", "title", "report_data", "generated_at"]
        read_only_fields = ["id", "generated_at"]


class SchoolDashboardView(APIView):
    permission_classes = [IsSchoolAdmin]

    def get(self, request):
        school = _get_school(request.user)
        batches = school.batches.filter(is_active=True)
        student_ids = list(BatchStudent.objects.filter(
            batch__school=school).values_list("student_id", flat=True).distinct())

        assessments_done = AssessmentResult.objects.filter(student_id__in=student_ids).count()
        career_profiles = CareerProfile.objects.filter(student_id__in=student_ids)
        avg_score = career_profiles.aggregate(avg=Avg("profile_score"))["avg"] or 0

        top_interests = {}
        for cp in career_profiles:
            for interest in (cp.career_interests or []):
                top_interests[interest] = top_interests.get(interest, 0) + 1

        return Response({
            "school": SchoolSerializer(school).data,
            "stats": {
                "total_batches": batches.count(),
                "total_students": len(student_ids),
                "assessments_completed": assessments_done,
                "avg_profile_score": round(avg_score, 1),
            },
            "top_career_interests": [
                {"interest": k, "count": v}
                for k, v in sorted(top_interests.items(), key=lambda x: -x[1])[:5]
            ],
            "recent_batches": BatchSerializer(batches[:5], many=True).data,
        })


class BatchListView(APIView):
    permission_classes = [IsSchoolAdmin]

    def get(self, request):
        school = _get_school(request.user)
        return Response(BatchSerializer(school.batches.all(), many=True).data)

    def post(self, request):
        school = _get_school(request.user)
        serializer = BatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        batch = serializer.save(school=school)
        return Response(BatchSerializer(batch).data, status=status.HTTP_201_CREATED)


class BatchDetailView(APIView):
    permission_classes = [IsSchoolAdmin]

    def _get_batch(self, pk, user):
        return get_object_or_404(StudentBatch, pk=pk, school=_get_school(user))

    def get(self, request, pk):
        batch = self._get_batch(pk, request.user)
        students = BatchStudent.objects.filter(batch=batch).select_related("student")
        student_ids = [bs.student_id for bs in students]
        assessments = AssessmentResult.objects.filter(student_id__in=student_ids)
        summary = {}
        for a in assessments:
            summary[a.assessment_type] = summary.get(a.assessment_type, 0) + 1
        return Response({
            "batch": BatchSerializer(batch).data,
            "students": BatchStudentSerializer(students, many=True).data,
            "assessment_completion": summary,
        })

    def patch(self, request, pk):
        batch = self._get_batch(pk, request.user)
        serializer = BatchSerializer(batch, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        batch = self._get_batch(pk, request.user)
        batch.is_active = False
        batch.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BatchStudentView(APIView):
    permission_classes = [IsSchoolAdmin]

    def post(self, request, pk):
        batch = get_object_or_404(StudentBatch, pk=pk, school=_get_school(request.user))
        serializer = BatchStudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bs = serializer.save(batch=batch)
        return Response(BatchStudentSerializer(bs).data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, student_id):
        batch = get_object_or_404(StudentBatch, pk=pk, school=_get_school(request.user))
        bs = get_object_or_404(BatchStudent, batch=batch, student_id=student_id)
        bs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SchoolStudentAnalyticsView(APIView):
    permission_classes = [IsSchoolAdmin]

    def get(self, request):
        school = _get_school(request.user)
        student_ids = list(BatchStudent.objects.filter(
            batch__school=school).values_list("student_id", flat=True).distinct())

        buckets = {"0-25": 0, "26-50": 0, "51-75": 0, "76-100": 0}
        top_careers = {}

        for cp in CareerProfile.objects.filter(student_id__in=student_ids):
            s = cp.profile_score or 0
            if s <= 25:
                buckets["0-25"] += 1
            elif s <= 50:
                buckets["26-50"] += 1
            elif s <= 75:
                buckets["51-75"] += 1
            else:
                buckets["76-100"] += 1
            for career in (cp.top_careers or []):
                top_careers[career] = top_careers.get(career, 0) + 1

        return Response({
            "total_students": len(student_ids),
            "profile_score_distribution": buckets,
            "top_career_aspirations": [
                {"career": k, "count": v}
                for k, v in sorted(top_careers.items(), key=lambda x: -x[1])[:8]
            ],
            "assessments_by_type": {
                t: AssessmentResult.objects.filter(student_id__in=student_ids, assessment_type=t).count()
                for t in ["interest", "personality", "aptitude", "readiness"]
            },
        })


class SchoolReportView(APIView):
    permission_classes = [IsSchoolAdmin]

    def get(self, request):
        school = _get_school(request.user)
        return Response(SchoolReportSerializer(school.reports.all()[:20], many=True).data)

    def post(self, request):
        school = _get_school(request.user)
        serializer = SchoolReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        report = serializer.save(school=school, generated_by=request.user)
        return Response(SchoolReportSerializer(report).data, status=status.HTTP_201_CREATED)


class ParentPortalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ParentProfileSerializer(
            ParentProfile.objects.filter(student=request.user), many=True).data)

    def post(self, request):
        serializer = ParentProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        parent = serializer.save(student=request.user)
        return Response(ParentProfileSerializer(parent).data, status=status.HTTP_201_CREATED)
