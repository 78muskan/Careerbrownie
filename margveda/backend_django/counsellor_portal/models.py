import uuid
from django.db import models
from django.conf import settings


class CounsellorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="counsellor_profile",
        limit_choices_to={"role": "counsellor"})
    bio = models.TextField(blank=True)
    tagline = models.CharField(max_length=200, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    specializations = models.JSONField(default=list)  # ["Career Counselling", "Study Abroad"]
    education = models.JSONField(default=list)  # [{"degree": "MBA", "institute": "IIM"}]
    certifications = models.JSONField(default=list)
    languages = models.JSONField(default=list)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    free_session_minutes = models.PositiveIntegerField(default=30)
    linkedin_url = models.URLField(blank=True)
    total_sessions_conducted = models.PositiveIntegerField(default=0)
    total_students_guided = models.PositiveIntegerField(default=0)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    is_accepting_students = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name} (Counsellor)"


class TimeSlot(models.Model):
    WEEKDAYS = [(i, d) for i, d in enumerate(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    counsellor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="time_slots", limit_choices_to={"role__in": ["counsellor", "admin"]})
    weekday = models.PositiveSmallIntegerField(choices=WEEKDAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ["counsellor", "weekday", "start_time"]
        ordering = ["weekday", "start_time"]

    def __str__(self):
        return f"{self.counsellor.full_name} — {self.get_weekday_display()} {self.start_time}"


class Appointment(models.Model):
    STATUS = [
        ("available", "Available"),
        ("requested", "Requested"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("no_show", "No Show"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    counsellor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="appointments", limit_choices_to={"role__in": ["counsellor", "admin"]})
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="booked_appointments", null=True, blank=True, limit_choices_to={"role": "student"})
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL, null=True, blank=True)
    scheduled_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    status = models.CharField(max_length=20, choices=STATUS, default="available")
    session_type = models.CharField(max_length=50, default="career_counselling")
    meeting_link = models.URLField(blank=True)
    google_event_id = models.CharField(max_length=200, blank=True)
    student_notes = models.TextField(blank=True)
    is_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["scheduled_date", "start_time"]

    def __str__(self):
        return f"{self.counsellor.full_name} x {self.student.full_name if self.student else 'Open'} — {self.scheduled_date}"


class SessionNote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="session_note")
    counsellor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="session_notes")
    key_points = models.TextField(blank=True)
    action_items = models.JSONField(default=list)  # [{"task": "...", "deadline": "..."}]
    resources_shared = models.JSONField(default=list)
    student_feedback = models.TextField(blank=True)
    student_rating = models.PositiveSmallIntegerField(null=True, blank=True)
    next_session_notes = models.TextField(blank=True)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notes — {self.appointment}"


class CounsellorRevenue(models.Model):
    counsellor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="revenue_records")
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="revenue")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, default="pending",
        choices=[("pending", "Pending"), ("paid", "Paid"), ("refunded", "Refunded")])
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.net_amount = self.amount - self.platform_fee
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.counsellor.full_name} — ₹{self.net_amount}"
