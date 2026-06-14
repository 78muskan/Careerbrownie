from django.contrib import admin
from .models import Resume, ResumeSection, ATSAnalysis


class ResumeSectionInline(admin.TabularInline):
    model = ResumeSection
    extra = 0
    fields = ["section_type", "title", "order"]


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ["title", "student", "template", "is_primary", "updated_at"]
    list_filter = ["template", "is_primary"]
    search_fields = ["student__email", "title"]
    inlines = [ResumeSectionInline]


@admin.register(ATSAnalysis)
class ATSAnalysisAdmin(admin.ModelAdmin):
    list_display = ["resume", "ats_score", "grade", "domain", "created_at"]
    list_filter = ["grade", "domain"]
    readonly_fields = ["ats_score", "grade", "breakdown", "matched_keywords",
                       "missing_keywords", "suggestions", "word_count", "created_at"]
