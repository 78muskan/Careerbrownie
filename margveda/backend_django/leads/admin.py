from django.contrib import admin
from .models import ContactLead, ConsultationBooking, NewsletterSubscriber


@admin.register(ContactLead)
class ContactLeadAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "source", "is_contacted", "created_at"]
    list_filter = ["source", "is_contacted", "created_at"]
    search_fields = ["name", "email", "phone", "subject"]
    list_editable = ["is_contacted"]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]


@admin.register(ConsultationBooking)
class ConsultationBookingAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "service", "preferred_date", "preferred_time", "status", "created_at"]
    list_filter = ["status", "service", "preferred_date"]
    search_fields = ["name", "email", "phone"]
    list_editable = ["status"]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "is_active", "subscribed_at"]
    list_filter = ["is_active"]
    search_fields = ["email", "name"]
    list_editable = ["is_active"]
