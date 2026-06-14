from django.db import models
from django.conf import settings


class StudentProfile(models.Model):
    STREAM_CHOICES = [
        ("science_pcm", "Science (PCM)"),
        ("science_pcb", "Science (PCB)"),
        ("science_pcmb", "Science (PCMB)"),
        ("commerce", "Commerce"),
        ("arts", "Arts / Humanities"),
        ("vocational", "Vocational"),
        ("other", "Other"),
    ]

    EDUCATION_CHOICES = [
        ("class_9_10", "Class 9-10"),
        ("class_11_12", "Class 11-12"),
        ("undergraduate", "Undergraduate"),
        ("postgraduate", "Postgraduate"),
        ("graduate", "Graduate (Working)"),
        ("professional", "Working Professional"),
        ("other", "Other"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile"
    )
    # Academic
    current_education = models.CharField(max_length=30, choices=EDUCATION_CHOICES, blank=True)
    stream = models.CharField(max_length=30, choices=STREAM_CHOICES, blank=True)
    institution_name = models.CharField(max_length=300, blank=True)
    graduation_year = models.PositiveIntegerField(null=True, blank=True)
    percentage_cgpa = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)

    # Career
    career_interests = models.JSONField(default=list, blank=True)
    preferred_industries = models.JSONField(default=list, blank=True)
    target_roles = models.JSONField(default=list, blank=True)

    # Skills
    technical_skills = models.JSONField(default=list, blank=True)
    soft_skills = models.JSONField(default=list, blank=True)
    certifications = models.JSONField(default=list, blank=True)
    languages = models.JSONField(default=list, blank=True)

    # Goals
    short_term_goal = models.TextField(blank=True)
    long_term_goal = models.TextField(blank=True)
    preferred_work_style = models.CharField(max_length=50, blank=True)
    salary_expectation = models.CharField(max_length=100, blank=True)
    study_abroad_interest = models.BooleanField(default=False)

    # Profile completeness (0-100)
    profile_score = models.PositiveIntegerField(default=0)
    onboarding_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"

    def __str__(self):
        return f"Profile: {self.user.full_name}"

    def calculate_score(self):
        fields = [
            self.current_education, self.stream, self.institution_name,
            self.city, bool(self.career_interests), bool(self.technical_skills),
            bool(self.soft_skills), self.short_term_goal, self.long_term_goal,
            bool(self.target_roles),
        ]
        filled = sum(1 for f in fields if f)
        score = int((filled / len(fields)) * 100)
        self.profile_score = score
        self.save(update_fields=["profile_score"])
        return score


class CareerProfile(models.Model):
    student = models.OneToOneField(
        StudentProfile, on_delete=models.CASCADE, related_name="career_profile"
    )
    career_score = models.PositiveIntegerField(default=0)
    ai_career_recommendations = models.JSONField(default=list, blank=True)
    skill_gaps = models.JSONField(default=list, blank=True)
    recommended_courses = models.JSONField(default=list, blank=True)
    career_roadmap = models.JSONField(default=dict, blank=True)
    personality_type = models.CharField(max_length=10, blank=True)
    assessment_completed = models.BooleanField(default=False)
    last_ai_analysis = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Career Profile: {self.student.user.full_name}"


class Goal(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("dropped", "Dropped"),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="goals")
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    target_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    is_ai_suggested = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["target_date", "-created_at"]

    def __str__(self):
        return f"{self.title} ({self.status})"
