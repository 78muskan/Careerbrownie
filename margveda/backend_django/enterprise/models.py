import uuid
from django.db import models
from users.models import User


class EnterpriseClient(models.Model):
    CLIENT_TYPE_CHOICES = [
        ("school", "School"),
        ("university", "University"),
        ("corporate", "Corporate"),
        ("government", "Government Institution"),
        ("ngo", "NGO / Non-profit"),
    ]
    LICENSE_CHOICES = [
        ("starter", "Starter"),
        ("growth", "Growth"),
        ("scale", "Scale"),
        ("unlimited", "Unlimited"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=300)
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPE_CHOICES)
    contact_name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    license_type = models.CharField(max_length=20, choices=LICENSE_CHOICES, default="starter")
    license_expiry = models.DateField(null=True, blank=True)
    max_users = models.PositiveIntegerField(default=50)
    current_users = models.PositiveIntegerField(default=0)
    contract_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.client_type}) — {self.license_type}"


class AICareerTwinSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ai_twin_sessions",
                                limit_choices_to={"role": "student"})
    session_context = models.JSONField(default=dict)
    career_profile_snapshot = models.JSONField(default=dict)
    recommendations = models.JSONField(default=list)
    action_plan = models.JSONField(default=list)
    predicted_placement_score = models.PositiveSmallIntegerField(default=0)
    predicted_career_fit = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"AI Twin session — {self.student.full_name} ({self.created_at.date()})"


class VoiceCounsellorScript(models.Model):
    TOPIC_CHOICES = [
        ("career_intro", "Career Introduction"),
        ("stream_selection", "Stream Selection"),
        ("college_options", "College Options"),
        ("exam_prep", "Exam Preparation"),
        ("skill_building", "Skill Building"),
        ("placement_ready", "Placement Readiness"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.CharField(max_length=30, choices=TOPIC_CHOICES, unique=True)
    script_text = models.TextField()
    follow_up_questions = models.JSONField(default=list)
    response_templates = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Voice Script — {self.topic}"


class AIVideoInterviewQuestion(models.Model):
    DIFFICULTY_CHOICES = [("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")]
    CATEGORY_CHOICES = [
        ("intro", "Introduction"),
        ("behavioral", "Behavioral"),
        ("situational", "Situational"),
        ("technical", "Technical"),
        ("motivation", "Motivation"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_text = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default="medium")
    ideal_answer_keywords = models.JSONField(default=list)
    time_limit_seconds = models.PositiveSmallIntegerField(default=120)
    tips = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.category}] {self.question_text[:60]}..."


class AIPlacementPrediction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="placement_predictions",
                                limit_choices_to={"role": "student"})
    placement_probability = models.FloatField(default=0.0)
    predicted_package_min = models.PositiveIntegerField(null=True, blank=True)
    predicted_package_max = models.PositiveIntegerField(null=True, blank=True)
    top_matching_companies = models.JSONField(default=list)
    skill_gap_impact = models.JSONField(default=dict)
    timeline_to_ready = models.PositiveSmallIntegerField(default=6)
    model_inputs = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student.full_name} — {round(self.placement_probability * 100)}% placement probability"
