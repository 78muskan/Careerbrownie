from django.urls import path
from .views import BookSessionView, StudentSessionsView, SessionDetailView, CounsellorSessionsView

urlpatterns = [
    path("book/", BookSessionView.as_view(), name="session-book"),
    path("my/", StudentSessionsView.as_view(), name="my-sessions"),
    path("<uuid:pk>/", SessionDetailView.as_view(), name="session-detail"),
    path("counsellor/", CounsellorSessionsView.as_view(), name="counsellor-sessions"),
    path("counsellor/<uuid:pk>/", CounsellorSessionsView.as_view(), name="counsellor-session-update"),
]
