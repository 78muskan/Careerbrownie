from django.urls import path
from .views import (
    QuestionsView, InterviewSessionListView,
    InterviewSessionDetailView, InterviewStatsView,
)

urlpatterns = [
    path("questions/", QuestionsView.as_view()),
    path("sessions/", InterviewSessionListView.as_view()),
    path("sessions/<uuid:pk>/", InterviewSessionDetailView.as_view()),
    path("stats/", InterviewStatsView.as_view()),
]
