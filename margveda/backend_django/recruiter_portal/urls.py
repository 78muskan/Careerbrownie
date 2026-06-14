from django.urls import path
from .views import (
    PublicJobListView, JobDetailView,
    RecruiterDashboardView, RecruiterJobView, RecruiterJobDetailView,
    RecruiterInternshipView, CandidateSearchView,
    ApplicationView, ApplicationDetailView,
    PlacementReadinessView, StudentJobMatchView,
)

urlpatterns = [
    # Public
    path("jobs/", PublicJobListView.as_view()),
    path("jobs/<uuid:pk>/", JobDetailView.as_view()),
    # Recruiter portal
    path("recruiter/dashboard/", RecruiterDashboardView.as_view()),
    path("recruiter/jobs/", RecruiterJobView.as_view()),
    path("recruiter/jobs/<uuid:pk>/", RecruiterJobDetailView.as_view()),
    path("recruiter/internships/", RecruiterInternshipView.as_view()),
    path("recruiter/candidates/", CandidateSearchView.as_view()),
    # Student
    path("applications/", ApplicationView.as_view()),
    path("applications/<uuid:pk>/", ApplicationDetailView.as_view()),
    path("placement-readiness/", PlacementReadinessView.as_view()),
    path("my-matches/", StudentJobMatchView.as_view()),
]
