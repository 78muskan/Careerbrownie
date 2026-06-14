from django.db import models
from django.conf import settings
import uuid


class Session(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled_student", "Cancelled by Student"),
        ("cancelled_counsellor", "Cancelled by Counsellor"),
        ("no_show", "No Show"),
    ]

    TYPE_CHOICES = [
        ("career_counselling", "Career Counselling"),
        ("university_admissions", "University Admissions"),
        ("study_abroad", "Study Abroad"),
        ("career_intelligence", "Career Intelligence"),
        ("ai_guidance", "AI Guidance"),
        ("follow_up", "Follow-up"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_sessions",
        limit_choices_to={"role": "student"},
    )
    counsellor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="counsellor_sessions",
        limit_choices_to={"role": "counsellor"},
    )
    session_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default="career_counselling")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="pending")
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    meeting_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    student_feedback = models.TextField(blank=True)
    student_rating = models.PositiveSmallIntegerField(null=True, blank=True)
    counsellor_notes = models.TextField(blank=True)
    recording_url = models.URLField(blank=True)
    is_free_session = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-scheduled_at"]
        verbose_name = "Session"
        verbose_name_plural = "Sessions"

    def __str__(self):
        return f"{self.student.full_name} → {self.get_session_type_display()} ({self.status})"


class CounsellorAvailability(models.Model):
    WEEKDAY_CHOICES = [
        (0, "Monday"), (1, "Tuesday"), (2, "Wednesday"),
        (3, "Thursday"), (4, "Friday"), (5, "Saturday"), (6, "Sunday"),
    ]

    counsellor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="availability_slots",
    )
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ["counsellor", "weekday", "start_time"]
        ordering = ["weekday", "start_time"]

    def __str__(self):
        return f"{self.counsellor.full_name} — {self.get_weekday_display()} {self.start_time}–{self.end_time}"
