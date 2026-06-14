from django.urls import path
from .views import CounsellorListView, TestimonialListView, FAQListView, UniversityPartnerListView

urlpatterns = [
    path("counsellors/", CounsellorListView.as_view(), name="counsellors"),
    path("testimonials/", TestimonialListView.as_view(), name="testimonials"),
    path("faqs/", FAQListView.as_view(), name="faqs"),
    path("universities/", UniversityPartnerListView.as_view(), name="universities"),
]
