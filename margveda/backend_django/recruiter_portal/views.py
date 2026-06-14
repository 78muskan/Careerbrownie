from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.db.models import Q

from .models import Company, RecruiterProfile, JobPosting, InternshipPosting, JobApplication, PlacementReadiness
from students.models import CareerProfile
from ai_engine.models import AssessmentResult
from ai_engine.scoring import generate_skill_gaps


class IsRecruiter(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and hasattr(request.user, "recruiter_profile")


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "slug", "industry", "description", "website",
                  "city", "employee_size", "is_verified", "is_active"]
        read_only_fields = ["id", "slug"]

    def create(self, validated_data):
        validated_data["slug"] = slugify(validated_data["name"])
        return super().create(validated_data)


class JobPostingSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)
    company_industry = serializers.CharField(source="company.industry", read_only=True)

    class Meta:
        model = JobPosting
        fields = ["id", "title", "description", "requirements", "skills_required",
                  "location", "job_type", "experience_level", "salary_min", "salary_max",
                  "domain", "deadline", "is_active", "views_count", "created_at",
                  "company_name", "company_industry"]
        read_only_fields = ["id", "views_count", "created_at"]


class InternshipSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = InternshipPosting
        fields = ["id", "title", "description", "skills_required", "location",
                  "is_remote", "duration_months", "stipend_monthly", "domain",
                  "deadline", "is_active", "created_at", "company_name"]
        read_only_fields = ["id", "created_at"]


class JobApplicationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    student_email = serializers.CharField(source="student.email", read_only=True)
    job_title = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = ["id", "status", "cover_letter", "resume_url", "notes",
                  "applied_at", "updated_at", "student_name", "student_email",
                  "job_title", "job", "internship"]
        read_only_fields = ["id", "applied_at", "updated_at", "student_name", "student_email"]

    def get_job_title(self, obj):
        if obj.job:
            return obj.job.title
        if obj.internship:
            return obj.internship.title
        return ""


class PlacementReadinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacementReadiness
        fields = ["overall_score", "profile_score", "skills_score", "assessment_score",
                  "resume_score", "interview_score", "strengths", "improvement_areas",
                  "recommended_roles", "last_updated"]
        read_only_fields = ["overall_score", "last_updated"]


class PublicJobListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        domain = request.query_params.get("domain", "")
        search = request.query_params.get("q", "")
        location = request.query_params.get("location", "")

        jobs = JobPosting.objects.filter(is_active=True).select_related("company")
        internships = InternshipPosting.objects.filter(is_active=True).select_related("company")

        if domain:
            jobs = jobs.filter(domain=domain)
            internships = internships.filter(domain=domain)
        if search:
            jobs = jobs.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if location:
            jobs = jobs.filter(location__icontains=location)

        return Response({
            "jobs": JobPostingSerializer(jobs[:20], many=True).data,
            "internships": InternshipSerializer(internships[:10], many=True).data,
        })


class JobDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        job = get_object_or_404(JobPosting, pk=pk, is_active=True)
        job.views_count += 1
        job.save(update_fields=["views_count"])
        return Response(JobPostingSerializer(job).data)


class RecruiterDashboardView(APIView):
    permission_classes = [IsRecruiter]

    def get(self, request):
        company = request.user.recruiter_profile.company
        jobs = company.jobs.filter(is_active=True)
        internships = company.internships.filter(is_active=True)
        job_ids = list(jobs.values_list("id", flat=True))
        intern_ids = list(internships.values_list("id", flat=True))

        total_apps = JobApplication.objects.filter(
            Q(job_id__in=job_ids) | Q(internship_id__in=intern_ids)).count()
        shortlisted = JobApplication.objects.filter(
            Q(job_id__in=job_ids) | Q(internship_id__in=intern_ids), status="shortlisted").count()

        return Response({
            "company": CompanySerializer(company).data,
            "stats": {
                "active_jobs": jobs.count(),
                "active_internships": internships.count(),
                "total_applications": total_apps,
                "shortlisted": shortlisted,
            },
            "recent_jobs": JobPostingSerializer(jobs[:5], many=True).data,
        })


class RecruiterJobView(APIView):
    permission_classes = [IsRecruiter]

    def get(self, request):
        company = request.user.recruiter_profile.company
        return Response(JobPostingSerializer(company.jobs.all(), many=True).data)

    def post(self, request):
        company = request.user.recruiter_profile.company
        serializer = JobPostingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job = serializer.save(company=company, posted_by=request.user)
        return Response(JobPostingSerializer(job).data, status=status.HTTP_201_CREATED)


class RecruiterJobDetailView(APIView):
    permission_classes = [IsRecruiter]

    def _get_job(self, pk, user):
        return get_object_or_404(JobPosting, pk=pk, company=user.recruiter_profile.company)

    def patch(self, request, pk):
        job = self._get_job(pk, request.user)
        serializer = JobPostingSerializer(job, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        job = self._get_job(pk, request.user)
        job.is_active = False
        job.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecruiterInternshipView(APIView):
    permission_classes = [IsRecruiter]

    def get(self, request):
        return Response(InternshipSerializer(
            request.user.recruiter_profile.company.internships.all(), many=True).data)

    def post(self, request):
        company = request.user.recruiter_profile.company
        serializer = InternshipSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        internship = serializer.save(company=company, posted_by=request.user)
        return Response(InternshipSerializer(internship).data, status=status.HTTP_201_CREATED)


class CandidateSearchView(APIView):
    permission_classes = [IsRecruiter]

    def get(self, request):
        skills = request.query_params.get("skills", "")
        domain = request.query_params.get("domain", "")
        min_score = int(request.query_params.get("min_score", 0))

        profiles = CareerProfile.objects.select_related("student").filter(student__role="student")
        if domain:
            profiles = profiles.filter(career_domain__icontains=domain)

        results = []
        for p in profiles:
            if skills:
                required = [s.strip().lower() for s in skills.split(",")]
                student_skills = [s.lower() for s in (p.skills or [])]
                if not any(r in " ".join(student_skills) for r in required):
                    continue
            if (p.profile_score or 0) < min_score:
                continue
            results.append({
                "student_id": str(p.student.id),
                "name": p.student.full_name,
                "profile_score": p.profile_score,
                "top_careers": p.top_careers or [],
                "skills": (p.skills or [])[:8],
                "career_domain": p.career_domain,
            })

        return Response({"candidates": results[:30]})


class ApplicationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        apps = JobApplication.objects.filter(student=request.user).select_related("job", "internship")
        return Response(JobApplicationSerializer(apps, many=True).data)

    def post(self, request):
        serializer = JobApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        app = serializer.save(student=request.user)
        return Response(JobApplicationSerializer(app).data, status=status.HTTP_201_CREATED)


class ApplicationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        app = get_object_or_404(JobApplication, pk=pk)
        if app.student != request.user and not hasattr(request.user, "recruiter_profile"):
            return Response({"error": "Forbidden"}, status=403)
        serializer = JobApplicationSerializer(app, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PlacementReadinessView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        readiness, _ = PlacementReadiness.objects.get_or_create(student=request.user)
        try:
            cp = CareerProfile.objects.get(student=request.user)
            readiness.profile_score = cp.profile_score or 0
            readiness.skills_score = min(len(cp.skills or []) * 5, 100)
        except CareerProfile.DoesNotExist:
            pass
        readiness.assessment_score = min(
            AssessmentResult.objects.filter(student=request.user).count() * 25, 100)
        readiness.recalculate()
        return Response(PlacementReadinessSerializer(readiness).data)


class StudentJobMatchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cp = CareerProfile.objects.get(student=request.user)
            student_skills = [s.lower() for s in (cp.skills or [])]
            domain = cp.career_domain or "technology"
        except CareerProfile.DoesNotExist:
            student_skills, domain = [], "technology"

        def match_score(required):
            if not required or not student_skills:
                return 0
            req = [s.lower() for s in required]
            matched = sum(1 for r in req if any(r in s for s in student_skills))
            return round(matched / len(req) * 100)

        jobs = JobPosting.objects.filter(is_active=True, domain=domain).select_related("company")[:15]
        internships = InternshipPosting.objects.filter(is_active=True, domain=domain).select_related("company")[:10]

        return Response({
            "job_matches": sorted(
                [{**JobPostingSerializer(j).data, "match_score": match_score(j.skills_required)} for j in jobs],
                key=lambda x: -x["match_score"]),
            "internship_matches": sorted(
                [{**InternshipSerializer(i).data, "match_score": match_score(i.skills_required)} for i in internships],
                key=lambda x: -x["match_score"]),
        })
