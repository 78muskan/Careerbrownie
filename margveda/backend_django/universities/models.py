import uuid
from django.db import models
from users.models import User


class University(models.Model):
    TYPES = [
        ("engineering", "Engineering"),
        ("medical", "Medical"),
        ("management", "Management"),
        ("law", "Law"),
        ("arts_science", "Arts & Science"),
        ("general", "General"),
        ("foreign", "Foreign University"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=200)
    university_type = models.CharField(max_length=30, choices=TYPES)
    country = models.CharField(max_length=100, default="India")
    location = models.CharField(max_length=200, blank=True)
    nirf_rank = models.PositiveSmallIntegerField(null=True, blank=True)
    qs_rank = models.PositiveSmallIntegerField(null=True, blank=True)
    naac_grade = models.CharField(max_length=10, blank=True)
    established = models.PositiveSmallIntegerField(null=True, blank=True)
    fees_per_year_inr = models.PositiveIntegerField(null=True, blank=True)
    tuition_per_year_usd = models.PositiveIntegerField(null=True, blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    notable_for = models.JSONField(default=list)
    entrance_exams = models.JSONField(default=list)
    placements = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["nirf_rank", "qs_rank", "name"]
        verbose_name_plural = "Universities"

    def __str__(self):
        return self.name


class Scholarship(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=200)
    provider = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    value_description = models.CharField(max_length=300)
    value_inr = models.PositiveIntegerField(null=True, blank=True)
    value_usd = models.PositiveIntegerField(null=True, blank=True)
    eligibility = models.JSONField(default=list)
    fields_of_study = models.JSONField(default=list)
    deadline_month = models.PositiveSmallIntegerField(null=True, blank=True)
    is_merit_based = models.BooleanField(default=True)
    is_need_based = models.BooleanField(default=False)
    is_renewable = models.BooleanField(default=False)
    url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ScholarshipApplication(models.Model):
    STATUS_CHOICES = [
        ("saved", "Saved"),
        ("preparing", "Preparing"),
        ("submitted", "Submitted"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
        ("awarded", "Awarded"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scholarship_applications",
                                limit_choices_to={"role": "student"})
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="saved")
    deadline = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["student", "scholarship"]
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.student.full_name} → {self.scholarship.name}"
