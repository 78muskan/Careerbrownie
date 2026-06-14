from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import University, Scholarship, ScholarshipApplication
from .data import (INDIAN_UNIVERSITIES, STUDY_ABROAD_UNIVERSITIES,
                   PROGRAMS, SCHOLARSHIPS, EXAM_CUTOFFS)


class UniversityListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        uni_type = request.query_params.get("type", "")
        country = request.query_params.get("country", "")
        query = request.query_params.get("q", "").lower()

        all_unis = INDIAN_UNIVERSITIES + STUDY_ABROAD_UNIVERSITIES
        results = all_unis

        if uni_type:
            results = [u for u in results if u.get("type") == uni_type]
        if country:
            results = [u for u in results if u.get("country", "India").lower() == country.lower()]
        if query:
            results = [u for u in results if query in u["name"].lower() or
                       any(query in f.lower() for f in u.get("notable_for", []))]

        return Response({"count": len(results), "results": results})


class UniversityDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        all_unis = INDIAN_UNIVERSITIES + STUDY_ABROAD_UNIVERSITIES
        uni = next((u for u in all_unis if u["slug"] == slug), None)
        if not uni:
            return Response({"error": "University not found."}, status=404)

        # Attach relevant programs
        programs = [p for p in PROGRAMS if any(
            d in p.get("domains", []) for d in ["technology", "management", "data_science"]
        )][:4]
        return Response({**uni, "suggested_programs": programs})


class ProgramListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        level = request.query_params.get("level", "")
        domain = request.query_params.get("domain", "")
        results = PROGRAMS
        if level:
            results = [p for p in results if p["level"] == level]
        if domain:
            results = [p for p in results if domain in p.get("domains", [])]
        return Response({"count": len(results), "results": results})


class ScholarshipListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        merit = request.query_params.get("merit_based", "")
        need = request.query_params.get("need_based", "")
        country = request.query_params.get("country", "")
        results = SCHOLARSHIPS
        if merit:
            results = [s for s in results if s["merit_based"] == (merit == "true")]
        if need:
            results = [s for s in results if s["need_based"] == (need == "true")]
        if country:
            results = [s for s in results if country.lower() in s["country"].lower()]
        return Response({"count": len(results), "results": results})


class ScholarshipDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        sch = next((s for s in SCHOLARSHIPS if s["slug"] == slug), None)
        if not sch:
            return Response({"error": "Scholarship not found."}, status=404)
        return Response(sch)


class ScholarshipApplicationSerializer(serializers.ModelSerializer):
    scholarship_name = serializers.CharField(source="scholarship.name", read_only=True)

    class Meta:
        model = ScholarshipApplication
        fields = ["id", "scholarship", "scholarship_name", "status", "deadline", "notes",
                  "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class MyScholarshipApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        apps = ScholarshipApplication.objects.filter(student=request.user).select_related("scholarship")
        return Response(ScholarshipApplicationSerializer(apps, many=True).data)

    def post(self, request):
        scholarship_slug = request.data.get("scholarship_slug")
        sch = get_object_or_404(Scholarship, slug=scholarship_slug)
        app, created = ScholarshipApplication.objects.get_or_create(
            student=request.user, scholarship=sch,
            defaults={"notes": request.data.get("notes", "")}
        )
        if not created:
            app.status = request.data.get("status", app.status)
            app.notes = request.data.get("notes", app.notes)
            app.save()
        return Response(ScholarshipApplicationSerializer(app).data,
                        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class ScholarshipMatchView(APIView):
    """Match scholarships to a student's profile."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from students.models import CareerProfile
        try:
            career = request.user.career_profile
            domain = career.target_career or ""
        except Exception:
            domain = ""

        # Simple matching: return all scholarships + highlight relevant ones
        results = []
        for sch in SCHOLARSHIPS:
            match_score = 0
            if not sch["need_based"]:
                match_score += 30
            if domain and any(domain.lower() in f.lower() for f in sch["fields"]):
                match_score += 40
            if sch["merit_based"]:
                match_score += 30
            results.append({**sch, "match_score": match_score})

        results.sort(key=lambda x: x["match_score"], reverse=True)
        return Response({"results": results})


class ExamCutoffView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        exam = request.query_params.get("exam", "")
        if exam and exam in EXAM_CUTOFFS:
            return Response(EXAM_CUTOFFS[exam])
        return Response({"exams": list(EXAM_CUTOFFS.keys()), "data": EXAM_CUTOFFS})
