import uuid
from django.db import models
from users.models import User


class InterviewSession(models.Model):
    INTERVIEW_TYPES = [
        ("hr", "HR Interview"),
        ("behavioural", "Behavioural Interview"),
        ("technical", "Technical Interview"),
        ("mock", "Mock Interview"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interview_sessions",
                                limit_choices_to={"role": "student"})
    interview_type = models.CharField(max_length=20, choices=INTERVIEW_TYPES)
    domain = models.CharField(max_length=50, default="general")
    total_questions = models.PositiveSmallIntegerField(default=0)
    questions_answered = models.PositiveSmallIntegerField(default=0)
    overall_score = models.PositiveSmallIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.student.full_name} — {self.interview_type} ({self.started_at.date()})"


class InterviewResponse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name="responses")
    question_id = models.CharField(max_length=20)
    question_text = models.TextField()
    response_text = models.TextField()
    score = models.PositiveSmallIntegerField(default=0)
    feedback = models.JSONField(default=list)
    word_count = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        unique_together = ["session", "question_id"]

    def __str__(self):
        return f"{self.session} — {self.question_id}"
