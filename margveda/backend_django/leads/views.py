from django.db.models import Count
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactLead, ConsultationBooking, NewsletterSubscriber
from .serializers import (
    ContactLeadSerializer, ContactLeadListSerializer,
    ConsultationBookingSerializer, ConsultationBookingListSerializer,
    NewsletterSerializer, NewsletterListSerializer,
)


def _notify_admin(subject, body):
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])
    except Exception:
        pass


# ── Public endpoints (no auth) ────────────────────────────────────────────────

class ContactLeadView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ContactLeadSerializer(data=request.data)
        if serializer.is_valid():
            lead = serializer.save()
            _notify_admin(
                f"[Career Brownie] New Contact: {lead.name or lead.email}",
                f"Name: {lead.name}\nEmail: {lead.email}\nPhone: {lead.phone}\n"
                f"Subject: {lead.subject}\nMessage: {lead.message}\nSource: {lead.source}",
            )
            return Response(
                {"message": "Thank you! We'll get back to you within 2 hours."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsultationBookingView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ConsultationBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save()
            _notify_admin(
                f"[Career Brownie] New Consultation: {booking.name}",
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
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = NewsletterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            NewsletterSubscriber.objects.get_or_create(email=email)
            return Response({"message": "You're subscribed!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ── Admin endpoints (auth required) ───────────────────────────────────────────

class AdminStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        today = timezone.now().date()
        return Response({
            "total_leads": ContactLead.objects.count(),
            "total_bookings": ConsultationBooking.objects.count(),
            "total_subscribers": NewsletterSubscriber.objects.count(),
            "new_leads_today": ContactLead.objects.filter(created_at__date=today).count(),
            "pending_bookings": ConsultationBooking.objects.filter(status="pending").count(),
            "leads_by_source": dict(
                ContactLead.objects.values("source").annotate(c=Count("id")).values_list("source", "c")
            ),
            "bookings_by_status": dict(
                ConsultationBooking.objects.values("status").annotate(c=Count("id")).values_list("status", "c")
            ),
        })


class AdminLeadListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        status_filter = request.query_params.get("status")
        source_filter = request.query_params.get("source")
        search = request.query_params.get("search", "").strip()
        leads = ContactLead.objects.all()
        if status_filter == "contacted":
            leads = leads.filter(is_contacted=True)
        elif status_filter == "uncontacted":
            leads = leads.filter(is_contacted=False)
        if source_filter:
            leads = leads.filter(source=source_filter)
        if search:
            leads = leads.filter(name__icontains=search) | leads.filter(email__icontains=search)
        leads = leads.order_by("-created_at")
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 20))
        total = leads.count()
        items = leads[(page - 1) * page_size : page * page_size]
        return Response({
            "items": ContactLeadListSerializer(items, many=True).data,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        })


class AdminLeadDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            lead = ContactLead.objects.get(pk=pk)
            return Response(ContactLeadSerializer(lead).data)
        except ContactLead.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

    def patch(self, request, pk):
        try:
            lead = ContactLead.objects.get(pk=pk)
            serializer = ContactLeadSerializer(lead, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except ContactLead.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

    def delete(self, request, pk):
        try:
            lead = ContactLead.objects.get(pk=pk)
            lead.delete()
            return Response(status=204)
        except ContactLead.DoesNotExist:
            return Response({"error": "Not found"}, status=404)


class AdminBookingListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        status_filter = request.query_params.get("status")
        search = request.query_params.get("search", "").strip()
        bookings = ConsultationBooking.objects.all()
        if status_filter:
            bookings = bookings.filter(status=status_filter)
        if search:
            bookings = bookings.filter(name__icontains=search) | bookings.filter(email__icontains=search)
        bookings = bookings.order_by("-created_at")
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 20))
        total = bookings.count()
        items = bookings[(page - 1) * page_size : page * page_size]
        return Response({
            "items": ConsultationBookingListSerializer(items, many=True).data,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        })


class AdminBookingDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            booking = ConsultationBooking.objects.get(pk=pk)
            return Response(ConsultationBookingSerializer(booking).data)
        except ConsultationBooking.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

    def patch(self, request, pk):
        try:
            booking = ConsultationBooking.objects.get(pk=pk)
            serializer = ConsultationBookingSerializer(booking, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except ConsultationBooking.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

    def delete(self, request, pk):
        try:
            booking = ConsultationBooking.objects.get(pk=pk)
            booking.delete()
            return Response(status=204)
        except ConsultationBooking.DoesNotExist:
            return Response({"error": "Not found"}, status=404)


class AdminSubscriberListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        subscribers = NewsletterSubscriber.objects.all().order_by("-subscribed_at")
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 50))
        total = subscribers.count()
        items = subscribers[(page - 1) * page_size : page * page_size]
        return Response({
            "items": NewsletterListSerializer(items, many=True).data,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        })


class AdminSubscriberToggleView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            sub = NewsletterSubscriber.objects.get(pk=pk)
            sub.is_active = not sub.is_active
            sub.save()
            return Response({"is_active": sub.is_active})
        except NewsletterSubscriber.DoesNotExist:
            return Response({"error": "Not found"}, status=404)
