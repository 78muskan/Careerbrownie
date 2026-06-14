from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import InterviewSession, InterviewResponse
from .question_bank import get_questions_by_type, evaluate_response


class InterviewResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewResponse
        fields = ["id", "question_id", "question_text", "response_text",
                  "score", "feedback", "word_count", "created_at"]
        read_only_fields = ["id", "score", "feedback", "word_count", "created_at"]


class InterviewSessionSerializer(serializers.ModelSerializer):
    responses = InterviewResponseSerializer(many=True, read_only=True)

    class Meta:
        model = InterviewSession
        fields = ["id", "interview_type", "domain", "total_questions",
                  "questions_answered", "overall_score", "is_completed",
                  "started_at", "completed_at", "responses"]
        read_only_fields = ["id", "total_questions", "questions_answered",
                            "overall_score", "is_completed", "started_at", "completed_at"]


class QuestionsView(APIView):
    """GET /interview/questions/?type=hr&domain=technology"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        interview_type = request.query_params.get("type", "hr")
        domain = request.query_params.get("domain", "general")
        questions = get_questions_by_type(interview_type, domain)
        return Response({"questions": questions, "total": len(questions)})


class InterviewSessionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = InterviewSession.objects.filter(student=request.user)
        return Response(InterviewSessionSerializer(sessions, many=True).data)

    def post(self, request):
        interview_type = request.data.get("interview_type", "hr")
        domain = request.data.get("domain", "general")
        questions = get_questions_by_type(interview_type, domain)

        session = InterviewSession.objects.create(
            student=request.user,
            interview_type=interview_type,
            domain=domain,
            total_questions=len(questions),
        )
        return Response({
            **InterviewSessionSerializer(session).data,
            "questions": questions,
        }, status=status.HTTP_201_CREATED)


class InterviewSessionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_session(self, pk, user):
        return get_object_or_404(InterviewSession, pk=pk, student=user)

    def get(self, request, pk):
        return Response(InterviewSessionSerializer(self._get_session(pk, request.user)).data)

    def post(self, request, pk):
        """Submit a response to one question."""
        session = self._get_session(pk, request.user)
        if session.is_completed:
            return Response({"error": "Session already completed."}, status=400)

        question_id = request.data.get("question_id")
        question_text = request.data.get("question_text", "")
        response_text = request.data.get("response_text", "")

        if not question_id or not response_text:
            return Response({"error": "question_id and response_text are required."}, status=400)

        evaluation = evaluate_response({"category": session.interview_type, "id": question_id}, response_text)

        resp, created = InterviewResponse.objects.update_or_create(
            session=session,
            question_id=question_id,
            defaults={
                "question_text": question_text,
                "response_text": response_text,
                "score": evaluation["score"],
                "feedback": evaluation["feedback"],
                "word_count": evaluation["word_count"],
            }
        )

        answered = session.responses.count()
        session.questions_answered = answered
        avg_score = session.responses.values_list("score", flat=True)
        session.overall_score = round(sum(avg_score) / max(len(avg_score), 1))

        if answered >= session.total_questions:
            session.is_completed = True
            session.completed_at = timezone.now()

        session.save(update_fields=["questions_answered", "overall_score", "is_completed", "completed_at"])

        return Response({
            "response": InterviewResponseSerializer(resp).data,
            "session": InterviewSessionSerializer(session).data,
        })

    def patch(self, request, pk):
        """Manually complete a session."""
        session = self._get_session(pk, request.user)
        session.is_completed = True
        session.completed_at = timezone.now()
        avg_score = list(session.responses.values_list("score", flat=True))
        if avg_score:
            session.overall_score = round(sum(avg_score) / len(avg_score))
        session.save()
        return Response(InterviewSessionSerializer(session).data)


class InterviewStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = InterviewSession.objects.filter(student=request.user, is_completed=True)
        total = sessions.count()
        by_type = {}
        for s in sessions:
            by_type.setdefault(s.interview_type, []).append(s.overall_score)
        type_averages = {t: round(sum(scores) / len(scores)) for t, scores in by_type.items()}
        overall_avg = round(sum(s.overall_score for s in sessions) / max(total, 1))

        return Response({
            "total_sessions": total,
            "overall_average": overall_avg,
            "by_type": type_averages,
        })
