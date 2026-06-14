from django.urls import path
from .views import (
    UniversityListView, UniversityDetailView, ProgramListView,
    ScholarshipListView, ScholarshipDetailView,
    MyScholarshipApplicationsView, ScholarshipMatchView, ExamCutoffView,
)

urlpatterns = [
    path("", UniversityListView.as_view()),
    path("<slug:slug>/", UniversityDetailView.as_view()),
    path("programs/list/", ProgramListView.as_view()),
    path("scholarships/", ScholarshipListView.as_view()),
    path("scholarships/match/", ScholarshipMatchView.as_view()),
    path("scholarships/my-applications/", MyScholarshipApplicationsView.as_view()),
    path("scholarships/<slug:slug>/", ScholarshipDetailView.as_view()),
    path("cutoffs/", ExamCutoffView.as_view()),
]
