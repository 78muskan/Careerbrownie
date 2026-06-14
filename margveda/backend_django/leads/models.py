from django.db import models


class ContactLead(models.Model):
    SOURCE_CHOICES = [
        ("contact_page", "Contact Page"),
        ("book_consultation", "Book Consultation"),
        ("landing_page", "Landing Page"),
        ("newsletter", "Newsletter"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=300, blank=True)
    message = models.TextField(blank=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default="contact_page")
    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Lead"
        verbose_name_plural = "Contact Leads"

    def __str__(self):
        return f"{self.name or self.email} ({self.source})"


class ConsultationBooking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("no_show", "No Show"),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    grade = models.CharField(max_length=100)
    service = models.CharField(max_length=200)
    preferred_date = models.DateField()
    preferred_time = models.CharField(max_length=50)
    message = models.TextField(blank=True)
    source = models.CharField(max_length=50, default="book_consultation")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Consultation Booking"
        verbose_name_plural = "Consultation Bookings"

    def __str__(self):
        return f"{self.name} — {self.preferred_date} {self.preferred_time} ({self.status})"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-subscribed_at"]
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"

    def __str__(self):
        return self.email
