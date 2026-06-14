from django.contrib import admin
from .models import CounsellorProfile, TimeSlot, Appointment, SessionNote, CounsellorRevenue


@admin.register(CounsellorProfile)
class CounsellorProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "experience_years", "avg_rating", "is_accepting_students", "is_verified"]
    list_filter = ["is_accepting_students", "is_verified"]
    search_fields = ["user__email", "user__full_name"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ["counsellor", "weekday", "start_time", "end_time", "is_active"]
    list_filter = ["weekday", "is_active"]
    search_fields = ["counsellor__email"]


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["counsellor", "student", "scheduled_date", "start_time", "status", "is_free"]
    list_filter = ["status", "session_type", "is_free"]
    search_fields = ["counsellor__email", "student__email"]
    readonly_fields = ["id", "created_at", "updated_at"]
    ordering = ["-scheduled_date"]


@admin.register(SessionNote)
class SessionNoteAdmin(admin.ModelAdmin):
    list_display = ["counsellor", "appointment", "student_rating", "is_private", "created_at"]
    list_filter = ["is_private"]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(CounsellorRevenue)
class CounsellorRevenueAdmin(admin.ModelAdmin):
    list_display = ["counsellor", "amount", "platform_fee", "net_amount", "payment_status", "created_at"]
    list_filter = ["payment_status"]
    readonly_fields = ["net_amount", "created_at"]
