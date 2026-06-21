"""Unit tests for StudentService."""
import pytest
from datetime import datetime, timezone

from app.services.student_service import StudentService
from app.services.auth_service import AuthService
from app.schemas.auth import RegisterRequest, UserRole
from app.schemas.student import StudentProfileUpdate, SessionBookingRequest
from fastapi import HTTPException


def _make_student(db, email="stu@test.com"):
    svc = AuthService(db)
    return svc.register_user(RegisterRequest(
        full_name="Test Student",
        email=email,
        password="pass12345",
        role=UserRole.student,
    ))


def _make_counsellor(db, email="coun@test.com"):
    svc = AuthService(db)
    return svc.register_user(RegisterRequest(
        full_name="Test Counsellor",
        email=email,
        password="pass12345",
        role=UserRole.counsellor,
    ))


class TestStudentProfileService:
    def test_get_or_create_profile_returns_profile(self, db):
        user = _make_student(db, "prof1@test.com")
        svc = StudentService(db)
        profile = svc.get_or_create_profile(user)
        assert profile is not None
        assert profile.user_id == user.id

    def test_profile_auto_created_on_register(self, db):
        user = _make_student(db, "prof2@test.com")
        assert user.student_profile is not None

    def test_update_profile_fields(self, db):
        user = _make_student(db, "prof3@test.com")
        svc = StudentService(db)
        svc.update_profile(user, StudentProfileUpdate(
            grade="12",
            stream="Science",
            career_goal="Software Engineer",
            skills="Python,Java",
        ))
        db.refresh(user.student_profile)
        assert user.student_profile.grade == "12"
        assert user.student_profile.career_goal == "Software Engineer"

    def test_update_profile_partial_does_not_clear_other_fields(self, db):
        user = _make_student(db, "prof4@test.com")
        svc = StudentService(db)
        svc.update_profile(user, StudentProfileUpdate(grade="11", stream="Commerce"))
        svc.update_profile(user, StudentProfileUpdate(career_goal="CA"))
        db.refresh(user.student_profile)
        assert user.student_profile.stream == "Commerce"
        assert user.student_profile.career_goal == "CA"

    def test_dashboard_includes_profile_and_counts(self, db):
        user = _make_student(db, "prof5@test.com")
        svc = StudentService(db)
        dashboard = svc.get_dashboard(user)
        assert dashboard.profile is not None
        assert isinstance(dashboard.roadmap_count, int)
        assert isinstance(dashboard.upcoming_sessions, int)

    def test_dashboard_next_step_changes_when_goal_set(self, db):
        user = _make_student(db, "prof6@test.com")
        svc = StudentService(db)
        svc.update_profile(user, StudentProfileUpdate(career_goal="Doctor"))
        dashboard = svc.get_dashboard(user)
        assert "Doctor" in dashboard.recommended_next_step


class TestSessionBookingService:
    def test_book_session_with_valid_counsellor(self, db):
        student = _make_student(db, "stu_sess@test.com")
        counsellor = _make_counsellor(db, "coun_sess@test.com")
        svc = StudentService(db)
        session = svc.book_session(student, SessionBookingRequest(
            counsellor_id=counsellor.id,
            topic="Career guidance",
            scheduled_at=datetime(2027, 1, 15, 10, 0, tzinfo=timezone.utc),
            mode="online",
        ))
        assert session.id is not None
        assert session.student_id == student.id
        assert session.counsellor_id == counsellor.id
        assert session.status == "requested"

    def test_book_session_with_invalid_counsellor_raises_404(self, db):
        student = _make_student(db, "stu_bad@test.com")
        svc = StudentService(db)
        with pytest.raises(HTTPException) as exc:
            svc.book_session(student, SessionBookingRequest(
                counsellor_id=99999,
                topic="Test",
                mode="online",
            ))
        assert exc.value.status_code == 404
