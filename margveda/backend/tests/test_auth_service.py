"""Unit tests for AuthService — service layer only, no HTTP."""
import pytest
from fastapi import HTTPException

from app.services.auth_service import AuthService
from app.schemas.auth import RegisterRequest, LoginRequest, UserRole
from app.core.security import get_password_hash, verify_password


class TestPasswordHashing:
    def test_hash_and_verify_roundtrip(self):
        hashed = get_password_hash("mysecretpassword")
        assert verify_password("mysecretpassword", hashed) is True

    def test_wrong_password_rejected(self):
        hashed = get_password_hash("correct")
        assert verify_password("wrong", hashed) is False

    def test_empty_password_rejected(self):
        hashed = get_password_hash("password")
        assert verify_password("", hashed) is False

    def test_hash_is_not_plaintext(self):
        pw = "secret123"
        hashed = get_password_hash(pw)
        assert pw not in hashed

    def test_two_hashes_of_same_password_differ(self):
        """Salt must make each hash unique."""
        h1 = get_password_hash("same")
        h2 = get_password_hash("same")
        assert h1 != h2


class TestAuthServiceRegister:
    def test_register_student_creates_user_and_profile(self, db):
        service = AuthService(db)
        payload = RegisterRequest(
            full_name="Alice Sharma",
            email="alice@test.com",
            password="strongpass1",
            role=UserRole.student,
        )
        user = service.register_user(payload)
        assert user.id is not None
        assert user.email == "alice@test.com"
        assert user.role == "student"
        assert user.student_profile is not None

    def test_register_counsellor_creates_counsellor_profile(self, db):
        service = AuthService(db)
        payload = RegisterRequest(
            full_name="Bob Mehta",
            email="bob@test.com",
            password="strongpass1",
            role=UserRole.counsellor,
        )
        user = service.register_user(payload)
        assert user.counsellor_profile is not None
        assert user.student_profile is None

    def test_duplicate_email_raises_409(self, db):
        service = AuthService(db)
        payload = RegisterRequest(
            full_name="Carol",
            email="carol@test.com",
            password="strongpass1",
            role=UserRole.student,
        )
        service.register_user(payload)
        with pytest.raises(HTTPException) as exc:
            service.register_user(payload)
        assert exc.value.status_code == 409

    def test_password_is_hashed_in_db(self, db):
        service = AuthService(db)
        payload = RegisterRequest(
            full_name="Dave",
            email="dave@test.com",
            password="myplainpass",
            role=UserRole.student,
        )
        user = service.register_user(payload)
        assert user.hashed_password != "myplainpass"
        assert verify_password("myplainpass", user.hashed_password)

    def test_email_normalized_to_lowercase(self, db):
        service = AuthService(db)
        payload = RegisterRequest(
            full_name="Eve",
            email="EVE@TEST.COM",
            password="strongpass1",
            role=UserRole.student,
        )
        user = service.register_user(payload)
        assert user.email == "eve@test.com"


class TestAuthServiceAuthenticate:
    def test_correct_credentials_return_user(self, db):
        service = AuthService(db)
        service.register_user(RegisterRequest(
            full_name="Frank", email="frank@test.com",
            password="pass12345", role=UserRole.student,
        ))
        user = service.authenticate_user(LoginRequest(
            email="frank@test.com", password="pass12345"
        ))
        assert user is not None
        assert user.email == "frank@test.com"

    def test_wrong_password_returns_none(self, db):
        service = AuthService(db)
        service.register_user(RegisterRequest(
            full_name="Grace", email="grace@test.com",
            password="correct1234", role=UserRole.student,
        ))
        result = service.authenticate_user(LoginRequest(
            email="grace@test.com", password="wrongpass"
        ))
        assert result is None

    def test_nonexistent_email_returns_none(self, db):
        service = AuthService(db)
        result = service.authenticate_user(LoginRequest(
            email="nobody@test.com", password="anything"
        ))
        assert result is None

    def test_build_auth_response_contains_token_and_user(self, db):
        service = AuthService(db)
        user = service.register_user(RegisterRequest(
            full_name="Harry", email="harry@test.com",
            password="pass12345", role=UserRole.student,
        ))
        response = service.build_auth_response(user)
        assert response.access_token
        assert response.user.email == "harry@test.com"
        assert response.token_type == "bearer"
