import uuid
from django.db import models
from users.models import User


class PredictorResult(models.Model):
    EXAM_TYPES = [
        ("JEE Main", "JEE Main"),
        ("JEE Advanced", "JEE Advanced"),
        ("NEET-UG", "NEET-UG"),
        ("CAT", "CAT"),
        ("CUET", "CUET"),
        ("GATE", "GATE"),
        ("XAT", "XAT"),
        ("BITSAT", "BITSAT"),
    ]
    CATEGORY_CHOICES = [
        ("general", "General"),
        ("obc", "OBC"),
        ("sc", "SC"),
        ("st", "ST"),
        ("ews", "EWS"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="predictor_results",
                                null=True, blank=True, limit_choices_to={"role": "student"})
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    score = models.FloatField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default="general")
    state = models.CharField(max_length=100, blank=True)
    predicted_colleges = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.exam_type} {self.score} → {len(self.predicted_colleges)} colleges"
