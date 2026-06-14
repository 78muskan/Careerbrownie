from django.urls import path
from .views import (
    EnterpriseClientListView, EnterpriseClientDetailView,
    AICareerTwinView, VideoInterviewQuestionsView,
    PlacementPredictorView, EnterpriseStatsView,
)

urlpatterns = [
    # Admin
    path("clients/", EnterpriseClientListView.as_view()),
    path("clients/<uuid:pk>/", EnterpriseClientDetailView.as_view()),
    path("stats/", EnterpriseStatsView.as_view()),
    # AI features
    path("ai-twin/", AICareerTwinView.as_view()),
    path("video-interview/questions/", VideoInterviewQuestionsView.as_view()),
    path("placement-predictor/", PlacementPredictorView.as_view()),
]
