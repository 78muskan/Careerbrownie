from django.contrib import admin
from .models import Counsellor, Testimonial, FAQ, UniversityPartner


@admin.register(Counsellor)
class CounsellorAdmin(admin.ModelAdmin):
    list_display = ["name", "title", "specialization", "experience_years", "rating", "is_featured", "is_active", "display_order"]
    list_filter = ["is_active", "is_featured"]
    search_fields = ["name", "title", "specialization", "bio"]
    list_editable = ["is_featured", "is_active", "display_order"]
    readonly_fields = ["created_at"]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["student_name", "student_role", "rating", "is_featured", "display_order"]
    list_filter = ["rating", "is_featured"]
    search_fields = ["student_name", "content"]
    list_editable = ["is_featured", "display_order"]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ["question", "category", "is_active", "display_order"]
    list_filter = ["category", "is_active"]
    search_fields = ["question", "answer"]
    list_editable = ["is_active", "display_order"]


@admin.register(UniversityPartner)
class UniversityPartnerAdmin(admin.ModelAdmin):
    list_display = ["name", "country", "is_featured", "display_order"]
    list_filter = ["country", "is_featured"]
    search_fields = ["name"]
    list_editable = ["is_featured", "display_order"]
