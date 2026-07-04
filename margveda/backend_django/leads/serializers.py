from rest_framework import serializers
from .models import ContactLead, ConsultationBooking, NewsletterSubscriber


class ContactLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactLead
        fields = ["id", "name", "email", "phone", "subject", "message", "source", "created_at", "is_contacted", "notes"]
        read_only_fields = ["created_at"]


class ContactLeadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactLead
        fields = ["id", "name", "email", "phone", "source", "created_at", "is_contacted"]


class ConsultationBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationBooking
        fields = [
            "id", "name", "email", "phone", "grade",
            "service", "preferred_date", "preferred_time", "message", "source",
            "status", "created_at", "admin_notes",
        ]
        read_only_fields = ["created_at"]


class ConsultationBookingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationBooking
        fields = [
            "id", "name", "email", "phone", "service",
            "preferred_date", "preferred_time", "status", "created_at",
        ]


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ["email", "name"]


class NewsletterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ["id", "email", "name", "subscribed_at", "is_active"]
