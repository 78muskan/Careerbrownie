from django.urls import path
from .views import (
    SchoolDashboardView, BatchListView, BatchDetailView, BatchStudentView,
    SchoolStudentAnalyticsView, SchoolReportView, ParentPortalView,
)

urlpatterns = [
    path("dashboard/", SchoolDashboardView.as_view()),
    path("batches/", BatchListView.as_view()),
    path("batches/<uuid:pk>/", BatchDetailView.as_view()),
    path("batches/<uuid:pk>/students/", BatchStudentView.as_view()),
    path("batches/<uuid:pk>/students/<uuid:student_id>/", BatchStudentView.as_view()),
    path("analytics/", SchoolStudentAnalyticsView.as_view()),
    path("reports/", SchoolReportView.as_view()),
    path("parents/", ParentPortalView.as_view()),
]
