from django.urls import path
from .views import (
    CounsellorProfileView, PublicCounsellorListView, PublicCounsellorDetailView,
    TimeSlotView, TimeSlotDetailView,
    BookAppointmentView, CounsellorCalendarView, AppointmentDetailView,
    SessionNoteView, CounsellorReportsView,
)

urlpatterns = [
    # Counsellor authenticated portal
    path("profile/", CounsellorProfileView.as_view(), name="counsellor-portal-profile"),
    path("slots/", TimeSlotView.as_view(), name="counsellor-slots"),
    path("slots/<uuid:pk>/", TimeSlotDetailView.as_view(), name="counsellor-slot-detail"),
    path("calendar/", CounsellorCalendarView.as_view(), name="counsellor-calendar"),
    path("appointments/<uuid:pk>/", AppointmentDetailView.as_view(), name="appointment-detail"),
    path("appointments/<uuid:appointment_id>/notes/", SessionNoteView.as_view(), name="session-notes"),
    path("reports/", CounsellorReportsView.as_view(), name="counsellor-reports"),
    # Student-facing booking
    path("booking/", BookAppointmentView.as_view(), name="book-appointment"),
    path("booking/counsellors/", PublicCounsellorListView.as_view(), name="counsellors-public"),
    path("booking/counsellors/<int:pk>/", PublicCounsellorDetailView.as_view(), name="counsellor-public-detail"),
]
