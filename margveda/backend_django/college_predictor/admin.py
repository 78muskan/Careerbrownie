from django.contrib import admin
from .models import PredictorResult


@admin.register(PredictorResult)
class PredictorResultAdmin(admin.ModelAdmin):
    list_display = ["exam_type", "score", "category", "student", "created_at"]
    list_filter = ["exam_type", "category"]
    search_fields = ["student__email"]
    readonly_fields = ["predicted_colleges", "created_at"]
