from django.db import models
from django.conf import settings
import uuid


class Notification(models.Model):
    TYPE_CHOICES = [
        ("session_confirmed", "Session Confirmed"),
        ("session_reminder", "Session Reminder"),
        ("session_cancelled", "Session Cancelled"),
        ("profile_complete", "Profile Complete"),
        ("new_recommendation", "New Recommendation"),
        ("counsellor_message", "Counsellor Message"),
        ("system", "System"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default="system")
    title = models.CharField(max_length=300)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"{self.user.email}: {self.title}"

    @classmethod
    def create(cls, user, notification_type, title, message, link=""):
        return cls.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            link=link,
        )


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ("register", "Register"),
        ("login", "Login"),
        ("logout", "Logout"),
        ("password_reset", "Password Reset"),
        ("profile_update", "Profile Update"),
        ("session_booked", "Session Booked"),
        ("session_cancelled", "Session Cancelled"),
        ("ai_query", "AI Query"),
        ("admin_action", "Admin Action"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"

    def __str__(self):
        who = self.user.email if self.user else "anonymous"
        return f"{who} — {self.action} at {self.created_at:%Y-%m-%d %H:%M}"
