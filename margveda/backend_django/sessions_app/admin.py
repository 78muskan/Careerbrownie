from django.contrib import admin
from .models import Session, CounsellorAvailability


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ["id", "student", "counsellor", "session_type", "status", "scheduled_at", "is_free_session"]
    list_filter = ["session_type", "status", "is_free_session"]
    search_fields = ["student__email", "counsellor__email"]
    readonly_fields = ["id", "created_at", "updated_at"]
    ordering = ["-scheduled_at"]


@admin.register(CounsellorAvailability)
class CounsellorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ["counsellor", "weekday", "start_time", "end_time", "is_active"]
    list_filter = ["weekday", "is_active"]
    search_fields = ["counsellor__email", "counsellor__full_name"]
