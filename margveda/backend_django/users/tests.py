"""
Django unit + integration tests for Users app.
Covers: registration, login, logout, token refresh, me endpoint, password flows.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User


class TestUserModel(TestCase):
    def test_create_user_normalizes_email(self):
        user = User.objects.create_user(
            email="USER@EXAMPLE.COM",
            password="pass1234",
            full_name="Test User",
        )
        # Django's normalize_email lowercases only the domain part
        self.assertEqual(user.email.split("@")[1], "example.com")

    def test_create_superuser_sets_staff_and_superuser(self):
        user = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpass",
            full_name="Admin User",
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.role, "admin")

    def test_user_str_includes_email_and_role(self):
        user = User.objects.create_user(
            email="str@example.com",
            password="pass1234",
            full_name="Str Test",
        )
        assert "str@example.com" in str(user)
        assert user.role in str(user)

    def test_update_last_login_saves(self):
        user = User.objects.create_user(
            email="login_time@example.com",
            password="pass1234",
            full_name="Login Test",
        )
        self.assertIsNone(user.last_login_at)
        user.update_last_login()
        user.refresh_from_db()
        self.assertIsNotNone(user.last_login_at)

    def test_password_is_hashed(self):
        user = User.objects.create_user(
            email="hashed@example.com",
            password="plainpassword",
            full_name="Hash Test",
        )
        self.assertNotEqual(user.password, "plainpassword")
        self.assertTrue(user.check_password("plainpassword"))


class TestRegisterEndpoint(APITestCase):
    url = "/api/v1/auth/register/"

    def _payload(self, email="reg@api.test"):
        return {
            "full_name": "API User",
            "email": email,
            "password": "testpass123",
            "role": "student",
        }

    def test_register_returns_201_with_tokens(self):
        r = self.client.post(self.url, self._payload(), format="json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", r.data)
        self.assertIn("refresh", r.data)
        self.assertIn("user", r.data)

    def test_register_creates_user_in_db(self):
        self.client.post(self.url, self._payload("db@api.test"), format="json")
        self.assertTrue(User.objects.filter(email="db@api.test").exists())

    def test_register_duplicate_email_returns_400(self):
        self.client.post(self.url, self._payload("dup@api.test"), format="json")
        r = self.client.post(self.url, self._payload("dup@api.test"), format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_short_password_returns_400(self):
        payload = self._payload("short@api.test")
        payload["password"] = "ab"
        r = self.client.post(self.url, payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_invalid_role_returns_400(self):
        payload = self._payload("role@api.test")
        payload["role"] = "superadmin"
        r = self.client.post(self.url, payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_missing_fields_returns_400(self):
        r = self.client.post(self.url, {"email": "missing@api.test"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_counsellor_role_works(self):
        payload = self._payload("coun@api.test")
        payload["role"] = "counsellor"
        r = self.client.post(self.url, payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.data["user"]["role"], "counsellor")


class TestLoginEndpoint(APITestCase):
    url = "/api/v1/auth/login/"

    def setUp(self):
        self.user = User.objects.create_user(
            email="login@api.test",
            password="loginpass123",
            full_name="Login User",
        )

    def test_login_correct_creds_returns_200_with_tokens(self):
        r = self.client.post(self.url, {
            "email": "login@api.test",
            "password": "loginpass123",
        }, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertIn("access", r.data)
        self.assertIn("refresh", r.data)

    def test_login_wrong_password_returns_400(self):
        r = self.client.post(self.url, {
            "email": "login@api.test",
            "password": "wrongpassword",
        }, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_nonexistent_email_returns_400(self):
        r = self.client.post(self.url, {
            "email": "nobody@api.test",
            "password": "anypassword",
        }, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_updates_last_login_at(self):
        self.client.post(self.url, {
            "email": "login@api.test",
            "password": "loginpass123",
        }, format="json")
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.last_login_at)

    def test_login_deactivated_user_returns_400(self):
        self.user.is_active = False
        self.user.save()
        r = self.client.post(self.url, {
            "email": "login@api.test",
            "password": "loginpass123",
        }, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)


class TestMeEndpoint(APITestCase):
    url = "/api/v1/auth/me/"

    def setUp(self):
        self.user = User.objects.create_user(
            email="me@api.test",
            password="mepass123",
            full_name="Me User",
        )
        login_r = self.client.post("/api/v1/auth/login/", {
            "email": "me@api.test", "password": "mepass123"
        }, format="json")
        self.token = login_r.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_me_returns_user_data(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["email"], "me@api.test")

    def test_me_without_token_returns_401(self):
        self.client.credentials()
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_patch_updates_full_name(self):
        r = self.client.patch(self.url, {"full_name": "Updated Name"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.full_name, "Updated Name")


class TestLogoutEndpoint(APITestCase):
    url = "/api/v1/auth/logout/"

    def setUp(self):
        self.user = User.objects.create_user(
            email="logout@api.test",
            password="logoutpass",
            full_name="Logout User",
        )
        login_r = self.client.post("/api/v1/auth/login/", {
            "email": "logout@api.test", "password": "logoutpass"
        }, format="json")
        self.access = login_r.data["access"]
        self.refresh = login_r.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")

    def test_logout_returns_200(self):
        r = self.client.post(self.url, {"refresh": self.refresh}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_logout_without_auth_returns_401(self):
        self.client.credentials()
        r = self.client.post(self.url, {"refresh": self.refresh}, format="json")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)


class TestTokenRefreshEndpoint(APITestCase):
    url = "/api/v1/auth/token/refresh/"

    def test_refresh_with_valid_token_returns_new_access(self):
        user = User.objects.create_user(
            email="refresh@api.test",
            password="refreshpass",
            full_name="Refresh User",
        )
        login_r = self.client.post("/api/v1/auth/login/", {
            "email": "refresh@api.test", "password": "refreshpass"
        }, format="json")
        refresh_token = login_r.data["refresh"]
        r = self.client.post(self.url, {"refresh": refresh_token}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertIn("access", r.data)

    def test_refresh_with_invalid_token_returns_401(self):
        r = self.client.post(self.url, {"refresh": "invalidtoken"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)


class TestHealthEndpoint(APITestCase):
    def test_health_check(self):
        r = self.client.get("/api/v1/health/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["status"], "ok")
