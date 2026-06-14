from django.contrib import admin
from .models import University, Scholarship, ScholarshipApplication


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ["name", "university_type", "country", "nirf_rank", "qs_rank", "is_active"]
    list_filter = ["university_type", "country", "is_active"]
    search_fields = ["name", "location"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ["name", "provider", "country", "is_merit_based", "is_need_based", "deadline_month"]
    list_filter = ["country", "is_merit_based", "is_need_based", "is_renewable"]
    search_fields = ["name", "provider"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ScholarshipApplication)
class ScholarshipApplicationAdmin(admin.ModelAdmin):
    list_display = ["student", "scholarship", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["student__email", "scholarship__name"]
