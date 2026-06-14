from django.urls import path
from .views import StudentProfileView, StudentDashboardView, GoalView, GoalDetailView

urlpatterns = [
    path("profile/", StudentProfileView.as_view(), name="student-profile"),
    path("dashboard/", StudentDashboardView.as_view(), name="student-dashboard"),
    path("goals/", GoalView.as_view(), name="goals"),
    path("goals/<int:pk>/", GoalDetailView.as_view(), name="goal-detail"),
]
