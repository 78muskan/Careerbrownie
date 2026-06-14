from django.contrib import admin
from .models import Company, RecruiterProfile, JobPosting, InternshipPosting, JobApplication, PlacementReadiness


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "industry", "city", "employee_size", "is_verified", "is_active"]
    list_filter = ["industry", "is_verified", "is_active"]
    search_fields = ["name", "city"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "company", "designation", "is_verified"]
    search_fields = ["user__email", "company__name"]


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ["title", "company", "location", "job_type", "experience_level",
                    "is_active", "views_count", "created_at"]
    list_filter = ["job_type", "experience_level", "domain", "is_active"]
    search_fields = ["title", "company__name"]


@admin.register(InternshipPosting)
class InternshipPostingAdmin(admin.ModelAdmin):
    list_display = ["title", "company", "location", "duration_months", "stipend_monthly", "is_active"]
    list_filter = ["domain", "is_remote", "is_active"]
    search_fields = ["title", "company__name"]


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ["student", "job", "internship", "status", "applied_at"]
    list_filter = ["status"]
    search_fields = ["student__email"]


@admin.register(PlacementReadiness)
class PlacementReadinessAdmin(admin.ModelAdmin):
    list_display = ["student", "overall_score", "profile_score", "skills_score",
                    "assessment_score", "resume_score", "interview_score", "last_updated"]
    readonly_fields = ["overall_score", "last_updated"]
    search_fields = ["student__email"]
