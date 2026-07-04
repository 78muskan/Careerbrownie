from django.urls import path
from .views import (
    ContactLeadView, ConsultationBookingView, NewsletterView,
    AdminStatsView, AdminLeadListView, AdminLeadDetailView,
    AdminBookingListView, AdminBookingDetailView,
    AdminSubscriberListView, AdminSubscriberToggleView,
)

urlpatterns = [
    # Public endpoints
    path("contact/", ContactLeadView.as_view(), name="contact"),
    path("consultation/", ConsultationBookingView.as_view(), name="consultation"),
    path("newsletter/", NewsletterView.as_view(), name="newsletter"),
    # Admin endpoints
    path("admin/stats/", AdminStatsView.as_view(), name="admin-stats"),
    path("admin/leads/", AdminLeadListView.as_view(), name="admin-leads"),
    path("admin/leads/<int:pk>/", AdminLeadDetailView.as_view(), name="admin-lead-detail"),
    path("admin/bookings/", AdminBookingListView.as_view(), name="admin-bookings"),
    path("admin/bookings/<int:pk>/", AdminBookingDetailView.as_view(), name="admin-booking-detail"),
    path("admin/subscribers/", AdminSubscriberListView.as_view(), name="admin-subscribers"),
    path("admin/subscribers/<int:pk>/toggle/", AdminSubscriberToggleView.as_view(), name="admin-subscriber-toggle"),
]
