import uuid
from django.db import models
from users.models import User


class Company(models.Model):
    INDUSTRY_CHOICES = [
        ("technology", "Technology"),
        ("finance", "Finance & Banking"),
        ("consulting", "Consulting"),
        ("healthcare", "Healthcare"),
        ("education", "Education"),
        ("ecommerce", "E-Commerce"),
        ("manufacturing", "Manufacturing"),
        ("media", "Media & Entertainment"),
        ("government", "Government & PSU"),
        ("startup", "Startup"),
        ("other", "Other"),
    ]
    SIZE_CHOICES = [
        ("1-10", "1–10"),
        ("11-50", "11–50"),
        ("51-200", "51–200"),
        ("201-1000", "201–1000"),
        ("1000+", "1000+"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    industry = models.CharField(max_length=30, choices=INDUSTRY_CHOICES, default="technology")
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to="company_logos/", null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    employee_size = models.CharField(max_length=20, choices=SIZE_CHOICES, default="51-200")
    founded_year = models.PositiveSmallIntegerField(null=True, blank=True)
    linkedin_url = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ["name"]

    def __str__(self):
        return self.name


class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="recruiter_profile")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="recruiters")
    designation = models.CharField(max_length=100, default="HR Manager")
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} @ {self.company.name}"


class JobPosting(models.Model):
    JOB_TYPE_CHOICES = [
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("contract", "Contract"),
        ("freelance", "Freelance"),
        ("remote", "Remote"),
    ]
    EXPERIENCE_CHOICES = [
        ("fresher", "Fresher (0–1 yr)"),
        ("junior", "Junior (1–3 yrs)"),
        ("mid", "Mid-level (3–6 yrs)"),
        ("senior", "Senior (6+ yrs)"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    skills_required = models.JSONField(default=list)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default="full_time")
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default="fresher")
    salary_min = models.PositiveIntegerField(null=True, blank=True)
    salary_max = models.PositiveIntegerField(null=True, blank=True)
    domain = models.CharField(max_length=50, default="technology")
    deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} @ {self.company.name}"


class InternshipPosting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="internships")
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    skills_required = models.JSONField(default=list)
    location = models.CharField(max_length=200)
    is_remote = models.BooleanField(default=False)
    duration_months = models.PositiveSmallIntegerField(default=3)
    stipend_monthly = models.PositiveIntegerField(null=True, blank=True)
    domain = models.CharField(max_length=50, default="technology")
    deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} Internship @ {self.company.name}"


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ("applied", "Applied"),
        ("shortlisted", "Shortlisted"),
        ("interview", "Interview Scheduled"),
        ("offered", "Offer Received"),
        ("rejected", "Rejected"),
        ("withdrawn", "Withdrawn"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_applications",
                                limit_choices_to={"role": "student"})
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, null=True, blank=True,
                            related_name="applications")
    internship = models.ForeignKey(InternshipPosting, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="applications")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")
    cover_letter = models.TextField(blank=True)
    resume_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-applied_at"]

    def __str__(self):
        target = self.job or self.internship
        return f"{self.student.full_name} → {target}"


class PlacementReadiness(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name="placement_readiness",
                                   limit_choices_to={"role": "student"})
    overall_score = models.PositiveSmallIntegerField(default=0)
    profile_score = models.PositiveSmallIntegerField(default=0)
    skills_score = models.PositiveSmallIntegerField(default=0)
    assessment_score = models.PositiveSmallIntegerField(default=0)
    resume_score = models.PositiveSmallIntegerField(default=0)
    interview_score = models.PositiveSmallIntegerField(default=0)
    strengths = models.JSONField(default=list)
    improvement_areas = models.JSONField(default=list)
    recommended_roles = models.JSONField(default=list)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Placement Readiness Scores"

    def __str__(self):
        return f"{self.student.full_name} — Placement Score: {self.overall_score}"

    def recalculate(self):
        self.overall_score = round(
            self.profile_score * 0.2 +
            self.skills_score * 0.25 +
            self.assessment_score * 0.2 +
            self.resume_score * 0.2 +
            self.interview_score * 0.15
        )
        self.save()
