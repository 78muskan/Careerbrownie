from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Resume, ResumeSection, ATSAnalysis
from .ats_engine import score_resume
from .resume_data import RESUME_TEMPLATES


class ResumeSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeSection
        fields = ["id", "section_type", "title", "content", "order"]


class ResumeSerializer(serializers.ModelSerializer):
    sections = ResumeSectionSerializer(many=True, read_only=True)

    class Meta:
        model = Resume
        fields = ["id", "title", "template", "personal_info", "summary",
                  "target_domain", "is_primary", "sections", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ATSAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ATSAnalysis
        fields = ["id", "domain", "ats_score", "grade", "breakdown",
                  "matched_keywords", "missing_keywords", "suggestions",
                  "word_count", "created_at"]
        read_only_fields = fields


class ResumeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        resumes = Resume.objects.filter(student=request.user)
        return Response(ResumeSerializer(resumes, many=True).data)

    def post(self, request):
        data = request.data.copy()
        serializer = ResumeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        resume = serializer.save(student=request.user)
        return Response(ResumeSerializer(resume).data, status=status.HTTP_201_CREATED)


class ResumeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_resume(self, pk, user):
        return get_object_or_404(Resume, pk=pk, student=user)

    def get(self, request, pk):
        return Response(ResumeSerializer(self._get_resume(pk, request.user)).data)

    def patch(self, request, pk):
        resume = self._get_resume(pk, request.user)
        serializer = ResumeSerializer(resume, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        self._get_resume(pk, request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResumeSectionView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_resume(self, resume_id, user):
        return get_object_or_404(Resume, pk=resume_id, student=user)

    def post(self, request, resume_id):
        resume = self._get_resume(resume_id, request.user)
        serializer = ResumeSectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        section = serializer.save(resume=resume)
        return Response(ResumeSectionSerializer(section).data, status=status.HTTP_201_CREATED)

    def patch(self, request, resume_id, section_id):
        resume = self._get_resume(resume_id, request.user)
        section = get_object_or_404(ResumeSection, pk=section_id, resume=resume)
        serializer = ResumeSectionSerializer(section, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, resume_id, section_id):
        resume = self._get_resume(resume_id, request.user)
        section = get_object_or_404(ResumeSection, pk=section_id, resume=resume)
        section.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ATSAnalyzeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, resume_id):
        resume = get_object_or_404(Resume, pk=resume_id, student=request.user)
        job_description = request.data.get("job_description", "")
        domain = request.data.get("domain", resume.target_domain or "technology")

        result = score_resume(resume, job_description=job_description, domain=domain)

        analysis = ATSAnalysis.objects.create(
            resume=resume,
            job_description=job_description,
            domain=domain,
            **result,
        )
        return Response(ATSAnalysisSerializer(analysis).data, status=status.HTTP_201_CREATED)

    def get(self, request, resume_id):
        resume = get_object_or_404(Resume, pk=resume_id, student=request.user)
        analyses = resume.ats_analyses.all()[:5]
        return Response(ATSAnalysisSerializer(analyses, many=True).data)


class ResumeTemplatesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(RESUME_TEMPLATES)
