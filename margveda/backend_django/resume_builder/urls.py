from django.urls import path
from .views import (
    ResumeListView, ResumeDetailView, ResumeSectionView,
    ATSAnalyzeView, ResumeTemplatesView,
)

urlpatterns = [
    path("", ResumeListView.as_view()),
    path("templates/", ResumeTemplatesView.as_view()),
    path("<uuid:pk>/", ResumeDetailView.as_view()),
    path("<uuid:resume_id>/sections/", ResumeSectionView.as_view()),
    path("<uuid:resume_id>/sections/<uuid:section_id>/", ResumeSectionView.as_view()),
    path("<uuid:resume_id>/ats/", ATSAnalyzeView.as_view()),
]
