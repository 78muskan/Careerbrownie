from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactLead, ConsultationBooking, NewsletterSubscriber
from .serializers import ContactLeadSerializer, ConsultationBookingSerializer, NewsletterSerializer


def _notify_admin(subject, body):
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])
    except Exception:
        pass


class ContactLeadView(APIView):
    def post(self, request):
        serializer = ContactLeadSerializer(data=request.data)
        if serializer.is_valid():
            lead = serializer.save()
            _notify_admin(
                f"[MargVedA] New Contact: {lead.name or lead.email}",
                f"Name: {lead.name}\nEmail: {lead.email}\nPhone: {lead.phone}\n"
                f"Subject: {lead.subject}\nMessage: {lead.message}\nSource: {lead.source}",
            )
            return Response(
                {"message": "Thank you! We'll get back to you within 2 hours."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsultationBookingView(APIView):
    def post(self, request):
        serializer = ConsultationBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save()
            _notify_admin(
                f"[MargVedA] New Consultation: {booking.name}",
                f"Name: {booking.name}\nEmail: {booking.email}\nPhone: {booking.phone}\n"
                f"Grade: {booking.grade}\nService: {booking.service}\n"
                f"Date: {booking.preferred_date} at {booking.preferred_time}",
            )
            return Response(
                {"message": "Booking confirmed! Check your email for details."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsletterView(APIView):
    def post(self, request):
        serializer = NewsletterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            NewsletterSubscriber.objects.get_or_create(email=email)
            return Response({"message": "You're subscribed!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
