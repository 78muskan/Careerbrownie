import uuid
from django.db import models
from users.models import User


class Resume(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resumes",
                                limit_choices_to={"role": "student"})
    title = models.CharField(max_length=200, default="My Resume")
    template = models.CharField(max_length=50, default="modern_clean")
    personal_info = models.JSONField(default=dict)
    summary = models.TextField(blank=True)
    target_domain = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def save(self, *args, **kwargs):
        if self.is_primary:
            Resume.objects.filter(student=self.student, is_primary=True).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.full_name} — {self.title}"


class ResumeSection(models.Model):
    SECTION_TYPES = [
        ("experience", "Work Experience"),
        ("education", "Education"),
        ("skills", "Skills"),
        ("projects", "Projects"),
        ("certifications", "Certifications"),
        ("achievements", "Achievements"),
        ("languages", "Languages"),
        ("custom", "Custom"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="sections")
    section_type = models.CharField(max_length=30, choices=SECTION_TYPES)
    title = models.CharField(max_length=100)
    content = models.JSONField(default=list)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.resume} / {self.section_type}"


class ATSAnalysis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="ats_analyses")
    job_description = models.TextField(blank=True)
    domain = models.CharField(max_length=50, default="technology")
    ats_score = models.PositiveSmallIntegerField(default=0)
    grade = models.CharField(max_length=2, default="D")
    breakdown = models.JSONField(default=dict)
    matched_keywords = models.JSONField(default=list)
    missing_keywords = models.JSONField(default=list)
    suggestions = models.JSONField(default=list)
    word_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.resume} — ATS {self.ats_score}"
