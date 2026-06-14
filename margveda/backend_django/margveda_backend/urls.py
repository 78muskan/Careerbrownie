from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

admin.site.site_header = "MargVedA Admin"
admin.site.site_title = "MargVedA"
admin.site.index_title = "Career Intelligence Platform — Admin"


@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok", "service": "MargVedA Backend"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", health_check, name="health"),
    path("api/v1/leads/", include("leads.urls")),
    path("api/v1/blog/", include("blog.urls")),
    path("api/v1/", include("counsellors.urls")),
    # Phase 2
    path("api/v1/auth/", include("users.urls")),
    path("api/v1/student/", include("students.urls")),
    path("api/v1/sessions/", include("sessions_app.urls")),
    path("api/v1/notifications/", include("notifications.urls")),
    # Phase 3
    path("api/v1/ai/", include("ai_engine.urls")),
    # Phase 4 — counsellor portal + booking
    path("api/v1/portal/", include("counsellor_portal.urls")),
    # Phase 5 — Employability Platform
    path("api/v1/resume/", include("resume_builder.urls")),
    path("api/v1/interview/", include("interview_coach.urls")),
    # Phase 6 — University Consulting
    path("api/v1/universities/", include("universities.urls")),
    path("api/v1/predictor/", include("college_predictor.urls")),
    # Phase 7 — School Ecosystem
    path("api/v1/school/", include("school_portal.urls")),
    # Phase 8 — Recruiter & Placement Platform
    path("api/v1/jobs/", include("recruiter_portal.urls")),
    # Phase 9 — Enterprise & Advanced AI
    path("api/v1/enterprise/", include("enterprise.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
