from django.urls import path
from .views import ContactLeadView, ConsultationBookingView, NewsletterView

urlpatterns = [
    path("contact/", ContactLeadView.as_view(), name="contact"),
    path("consultation/", ConsultationBookingView.as_view(), name="consultation"),
    path("newsletter/", NewsletterView.as_view(), name="newsletter"),
]
