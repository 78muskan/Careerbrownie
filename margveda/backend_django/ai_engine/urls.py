from django.urls import path
from .views import (
    AssessmentQuestionsView, SubmitAssessmentView, AssessmentResultView,
    RoadmapView, AIAdvisorView, CareerDetailView, CareerListView, ChatView,
)

urlpatterns = [
    path("chat/", ChatView.as_view(), name="ai-chat"),
    path("assessment/<str:assessment_type>/questions/", AssessmentQuestionsView.as_view(), name="assessment-questions"),
    path("assessment/<str:assessment_type>/submit/", SubmitAssessmentView.as_view(), name="assessment-submit"),
    path("assessment/<str:assessment_type>/result/", AssessmentResultView.as_view(), name="assessment-result"),
    path("assessment/results/", AssessmentResultView.as_view(), name="all-assessment-results"),
    path("roadmap/", RoadmapView.as_view(), name="roadmap"),
    path("advisor/", AIAdvisorView.as_view(), name="ai-advisor"),
    path("careers/", CareerListView.as_view(), name="careers"),
    path("careers/<str:career_key>/", CareerDetailView.as_view(), name="career-detail"),
]
