from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from .models import Counsellor, Testimonial, FAQ, UniversityPartner


class CounsellorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counsellor
        fields = [
            "id", "name", "title", "specialization", "bio",
            "experience_years", "total_sessions", "rating",
            "photo", "tags", "linkedin_url", "is_featured",
        ]


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ["id", "student_name", "student_role", "content", "rating", "course", "photo", "is_featured"]


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ["id", "question", "answer", "category"]


class UniversityPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityPartner
        fields = ["id", "name", "country", "logo", "website", "is_featured"]


class CounsellorListView(APIView):
    def get(self, request):
        qs = Counsellor.objects.filter(is_active=True)
        featured = request.query_params.get("featured")
        if featured:
            qs = qs.filter(is_featured=True)
        return Response(CounsellorSerializer(qs, many=True).data)


class TestimonialListView(APIView):
    def get(self, request):
        qs = Testimonial.objects.all()
        featured = request.query_params.get("featured")
        if featured:
            qs = qs.filter(is_featured=True)
        return Response(TestimonialSerializer(qs, many=True).data)


class FAQListView(APIView):
    def get(self, request):
        qs = FAQ.objects.filter(is_active=True)
        category = request.query_params.get("category")
        if category:
            qs = qs.filter(category=category)
        return Response(FAQSerializer(qs, many=True).data)


class UniversityPartnerListView(APIView):
    def get(self, request):
        qs = UniversityPartner.objects.all()
        return Response(UniversityPartnerSerializer(qs, many=True).data)
