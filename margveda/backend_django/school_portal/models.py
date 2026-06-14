import uuid
from django.db import models
from users.models import User


class School(models.Model):
    PLAN_CHOICES = [
        ("free", "Free Trial"),
        ("basic", "Basic"),
        ("pro", "Professional"),
        ("enterprise", "Enterprise"),
    ]
    TYPE_CHOICES = [
        ("cbse", "CBSE"),
        ("icse", "ICSE"),
        ("state", "State Board"),
        ("ib", "IB"),
        ("igcse", "IGCSE"),
        ("other", "Other"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=300)
    code = models.CharField(max_length=20, unique=True)
    school_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="cbse")
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to="school_logos/", null=True, blank=True)
    subscription_plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default="free")
    max_students = models.PositiveIntegerField(default=100)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.city})"


class SchoolAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="school_admin_profile")
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="admins")
    designation = models.CharField(max_length=100, default="School Counsellor")
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} @ {self.school.name}"


class StudentBatch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="batches")
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=10, default="2025-26")
    class_teacher = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["grade", "name"]
        unique_together = ["school", "name", "academic_year"]

    def __str__(self):
        return f"{self.school.name} — {self.name} ({self.academic_year})"

    @property
    def student_count(self):
        return self.students.count()


class BatchStudent(models.Model):
    batch = models.ForeignKey(StudentBatch, on_delete=models.CASCADE, related_name="students")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="school_batches",
                                limit_choices_to={"role": "student"})
    roll_number = models.CharField(max_length=30, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["batch", "student"]

    def __str__(self):
        return f"{self.student.full_name} in {self.batch.name}"


class ParentProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="parents",
                                limit_choices_to={"role": "student"})
    parent_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    relationship = models.CharField(max_length=30, default="Parent")
    occupation = models.CharField(max_length=100, blank=True)
    is_portal_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.parent_name} (parent of {self.student.full_name})"


class SchoolReport(models.Model):
    REPORT_TYPES = [
        ("career", "Career Report"),
        ("assessment", "Assessment Report"),
        ("batch_analytics", "Batch Analytics"),
        ("parent", "Parent Report"),
        ("counselling", "Counselling Report"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="reports")
    batch = models.ForeignKey(StudentBatch, on_delete=models.SET_NULL, null=True, blank=True)
    report_type = models.CharField(max_length=30, choices=REPORT_TYPES)
    title = models.CharField(max_length=200)
    report_data = models.JSONField(default=dict)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-generated_at"]

    def __str__(self):
        return f"{self.school.name} — {self.title}"
