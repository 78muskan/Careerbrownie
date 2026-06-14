from django.urls import path
from .views import CollegePredictorView, SupportedExamsView, MyPredictionsView

urlpatterns = [
    path("predict/", CollegePredictorView.as_view()),
    path("exams/", SupportedExamsView.as_view()),
    path("my-predictions/", MyPredictionsView.as_view()),
]
