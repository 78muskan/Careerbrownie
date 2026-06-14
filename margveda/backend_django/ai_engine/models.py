import uuid
from django.db import models


class AssessmentResult(models.Model):
    TYPES = [
        ("interest", "Interest Assessment"),
        ("personality", "Personality Assessment"),
        ("aptitude", "Aptitude Assessment"),
        ("readiness", "Career Readiness"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey("students.StudentProfile", on_delete=models.CASCADE, related_name="assessment_results")
    assessment_type = models.CharField(max_length=20, choices=TYPES)
    responses = models.JSONField(default=dict)
    scores = models.JSONField(default=dict)
    result_summary = models.TextField(blank=True)
    top_careers = models.JSONField(default=list)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["student", "assessment_type"]
        ordering = ["-completed_at"]

    def __str__(self):
        return f"{self.student.user.full_name} — {self.assessment_type}"


class CareerRoadmap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.OneToOneField("students.StudentProfile", on_delete=models.CASCADE, related_name="roadmap")
    target_career = models.CharField(max_length=200)
    plan_3_months = models.JSONField(default=list)
    plan_6_months = models.JSONField(default=list)
    plan_1_year = models.JSONField(default=list)
    plan_3_years = models.JSONField(default=list)
    plan_5_years = models.JSONField(default=list)
    progress_notes = models.TextField(blank=True)
    generated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.user.full_name} → {self.target_career}"


class AIInsight(models.Model):
    TYPES = [
        ("career_match", "Career Match"),
        ("skill_gap", "Skill Gap"),
        ("learning_path", "Learning Path"),
        ("market_trend", "Market Trend"),
        ("salary_insight", "Salary Insight"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey("students.StudentProfile", on_delete=models.CASCADE, related_name="ai_insights")
    insight_type = models.CharField(max_length=20, choices=TYPES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    data = models.JSONField(default=dict)
    relevance_score = models.FloatField(default=0.0)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-relevance_score", "-generated_at"]
