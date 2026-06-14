from django.contrib import admin
from .models import AssessmentResult, CareerRoadmap, AIInsight


@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
    list_display = ["student", "assessment_type", "result_summary", "completed_at"]
    list_filter = ["assessment_type"]
    search_fields = ["student__user__email"]
    readonly_fields = ["id", "completed_at"]


@admin.register(CareerRoadmap)
class CareerRoadmapAdmin(admin.ModelAdmin):
    list_display = ["student", "target_career", "generated_at"]
    search_fields = ["student__user__email", "target_career"]
    readonly_fields = ["id", "generated_at"]


@admin.register(AIInsight)
class AIInsightAdmin(admin.ModelAdmin):
    list_display = ["student", "insight_type", "title", "relevance_score", "generated_at"]
    list_filter = ["insight_type"]
    search_fields = ["student__user__email", "title"]
    readonly_fields = ["id", "generated_at"]
