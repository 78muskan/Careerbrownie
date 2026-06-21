"""Integration tests for /api/v1/auth/* routes."""
import pytest


REGISTER_URL = "/api/v1/auth/register"
LOGIN_URL = "/api/v1/auth/login"
TOKEN_URL = "/api/v1/auth/token"
ME_URL = "/api/v1/auth/me"


def _register(client, email="user@routes.test", role="student"):
    return client.post(REGISTER_URL, json={
        "full_name": "Route User",
        "email": email,
        "password": "routepass1",
        "role": role,
    })


class TestRegisterRoute:
    def test_register_returns_201_with_token_and_user(self, client):
        r = _register(client, "new1@routes.test")
        assert r.status_code == 201
        data = r.json()
        assert "access_token" in data
        assert data["user"]["email"] == "new1@routes.test"
        assert data["user"]["role"] == "student"

    def test_register_duplicate_email_returns_409(self, client):
        _register(client, "dup@routes.test")
        r = _register(client, "dup@routes.test")
        assert r.status_code == 409

    def test_register_invalid_email_returns_422(self, client):
        r = client.post(REGISTER_URL, json={
            "full_name": "Bad Email",
            "email": "notanemail",
            "password": "pass12345",
            "role": "student",
        })
        assert r.status_code == 422

    def test_register_short_password_returns_422(self, client):
        r = client.post(REGISTER_URL, json={
            "full_name": "Short Pass",
            "email": "short@routes.test",
            "password": "abc",
            "role": "student",
        })
        assert r.status_code == 422

    def test_register_short_name_returns_422(self, client):
        r = client.post(REGISTER_URL, json={
            "full_name": "A",
            "email": "shortname@routes.test",
            "password": "pass12345",
            "role": "student",
        })
        assert r.status_code == 422

    def test_register_missing_fields_returns_422(self, client):
        r = client.post(REGISTER_URL, json={"email": "partial@routes.test"})
        assert r.status_code == 422

    def test_register_counsellor_role_works(self, client):
        r = _register(client, "coun1@routes.test", role="counsellor")
        assert r.status_code == 201
        assert r.json()["user"]["role"] == "counsellor"


class TestLoginRoute:
    def test_login_with_correct_creds_returns_200(self, client):
        _register(client, "login1@routes.test")
        r = client.post(LOGIN_URL, json={"email": "login1@routes.test", "password": "routepass1"})
        assert r.status_code == 200
        assert "access_token" in r.json()

    def test_login_wrong_password_returns_401(self, client):
        _register(client, "login2@routes.test")
        r = client.post(LOGIN_URL, json={"email": "login2@routes.test", "password": "wrongpass"})
        assert r.status_code == 401

    def test_login_nonexistent_email_returns_401(self, client):
        r = client.post(LOGIN_URL, json={"email": "nobody@routes.test", "password": "pass"})
        assert r.status_code == 401

    def test_login_response_user_matches_registered_user(self, client):
        _register(client, "login3@routes.test")
        r = client.post(LOGIN_URL, json={"email": "login3@routes.test", "password": "routepass1"})
        assert r.json()["user"]["email"] == "login3@routes.test"


class TestMeRoute:
    def test_me_with_valid_token_returns_user(self, client):
        _register(client, "me1@routes.test")
        token = client.post(LOGIN_URL, json={"email": "me1@routes.test", "password": "routepass1"}).json()["access_token"]
        r = client.get(ME_URL, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        assert r.json()["email"] == "me1@routes.test"

    def test_me_without_token_returns_401(self, client):
        r = client.get(ME_URL)
        assert r.status_code == 401

    def test_me_with_invalid_token_returns_401(self, client):
        r = client.get(ME_URL, headers={"Authorization": "Bearer invalid.token.here"})
        assert r.status_code == 401


class TestTokenRoute:
    def test_swagger_token_endpoint_works(self, client):
        _register(client, "tok1@routes.test")
        r = client.post(TOKEN_URL, data={
            "username": "tok1@routes.test",
            "password": "routepass1",
        })
        assert r.status_code == 200
        assert "access_token" in r.json()
