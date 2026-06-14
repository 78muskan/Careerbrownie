from django.contrib import admin
from .models import InterviewSession, InterviewResponse


class InterviewResponseInline(admin.TabularInline):
    model = InterviewResponse
    extra = 0
    readonly_fields = ["question_id", "score", "word_count", "created_at"]
    fields = ["question_id", "score", "word_count", "created_at"]


@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = ["student", "interview_type", "domain", "overall_score", "is_completed", "started_at"]
    list_filter = ["interview_type", "domain", "is_completed"]
    search_fields = ["student__email"]
    inlines = [InterviewResponseInline]
