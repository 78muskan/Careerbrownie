from django.db import models


class Counsellor(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=300)
    specialization = models.CharField(max_length=300)
    bio = models.TextField()
    experience_years = models.PositiveIntegerField(default=0)
    total_sessions = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)
    photo = models.ImageField(upload_to="counsellors/", null=True, blank=True)
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    linkedin_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "-rating"]
        verbose_name = "Counsellor"
        verbose_name_plural = "Counsellors"

    def __str__(self):
        return f"{self.name} — {self.title}"

    def tags_list(self):
        return [t.strip() for t in self.tags.split(",") if t.strip()]


class Testimonial(models.Model):
    student_name = models.CharField(max_length=200)
    student_role = models.CharField(max_length=300)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    course = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to="testimonials/", null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "-created_at"]
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.student_name} — {self.rating}★"


class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.CharField(max_length=100, default="General")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question[:80]


class UniversityPartner(models.Model):
    name = models.CharField(max_length=300)
    country = models.CharField(max_length=100, default="India")
    logo = models.ImageField(upload_to="universities/", null=True, blank=True)
    website = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name
