from rest_framework import serializers
from .models import ContactLead, ConsultationBooking, NewsletterSubscriber


class ContactLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactLead
        fields = ["id", "name", "email", "phone", "subject", "message", "source"]


class ConsultationBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationBooking
        fields = [
            "id", "name", "email", "phone", "grade",
            "service", "preferred_date", "preferred_time", "message", "source",
        ]


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ["email", "name"]
