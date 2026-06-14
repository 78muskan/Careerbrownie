from django.contrib import admin
from .models import (EnterpriseClient, AICareerTwinSession,
                     VoiceCounsellorScript, AIVideoInterviewQuestion, AIPlacementPrediction)


@admin.register(EnterpriseClient)
class EnterpriseClientAdmin(admin.ModelAdmin):
    list_display = ["name", "client_type", "license_type", "max_users", "current_users",
                    "contract_value", "is_active", "license_expiry"]
    list_filter = ["client_type", "license_type", "is_active"]
    search_fields = ["name", "contact_email", "city"]


@admin.register(AICareerTwinSession)
class AICareerTwinSessionAdmin(admin.ModelAdmin):
    list_display = ["student", "predicted_career_fit", "predicted_placement_score", "created_at"]
    search_fields = ["student__email"]
    readonly_fields = ["session_context", "career_profile_snapshot", "recommendations",
                       "action_plan", "predicted_placement_score", "predicted_career_fit", "created_at"]


@admin.register(VoiceCounsellorScript)
class VoiceCounsellorScriptAdmin(admin.ModelAdmin):
    list_display = ["topic", "is_active", "updated_at"]
    list_filter = ["is_active"]


@admin.register(AIVideoInterviewQuestion)
class AIVideoInterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "category", "difficulty", "time_limit_seconds", "is_active"]
    list_filter = ["category", "difficulty", "is_active"]
    search_fields = ["question_text"]


@admin.register(AIPlacementPrediction)
class AIPlacementPredictionAdmin(admin.ModelAdmin):
    list_display = ["student", "placement_probability", "predicted_package_min",
                    "predicted_package_max", "timeline_to_ready", "created_at"]
    readonly_fields = ["placement_probability", "predicted_package_min", "predicted_package_max",
                       "top_matching_companies", "skill_gap_impact", "model_inputs", "created_at"]
    search_fields = ["student__email"]
