from django.contrib import admin
from .models import School, SchoolAdmin, StudentBatch, BatchStudent, ParentProfile, SchoolReport


class BatchInline(admin.TabularInline):
    model = StudentBatch
    extra = 0
    fields = ["name", "grade", "academic_year", "is_active"]


@admin.register(School)
class SchoolAdmin_(admin.ModelAdmin):
    list_display = ["name", "city", "state", "school_type", "subscription_plan", "is_active", "joined_at"]
    list_filter = ["school_type", "subscription_plan", "state", "is_active"]
    search_fields = ["name", "city", "contact_email"]
    inlines = [BatchInline]


@admin.register(SchoolAdmin)
class SchoolAdminAdmin(admin.ModelAdmin):
    list_display = ["user", "school", "designation", "is_primary"]
    list_filter = ["is_primary"]
    search_fields = ["user__email", "school__name"]


@admin.register(StudentBatch)
class StudentBatchAdmin(admin.ModelAdmin):
    list_display = ["name", "school", "grade", "academic_year", "is_active"]
    list_filter = ["academic_year", "is_active"]
    search_fields = ["name", "school__name"]


@admin.register(BatchStudent)
class BatchStudentAdmin(admin.ModelAdmin):
    list_display = ["student", "batch", "roll_number", "joined_at"]
    search_fields = ["student__email", "batch__name"]


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ["parent_name", "student", "relationship", "email", "is_portal_enabled"]
    list_filter = ["relationship", "is_portal_enabled"]
    search_fields = ["parent_name", "email", "student__email"]


@admin.register(SchoolReport)
class SchoolReportAdmin(admin.ModelAdmin):
    list_display = ["title", "school", "report_type", "generated_at"]
    list_filter = ["report_type"]
    search_fields = ["title", "school__name"]
