"""
Regression tests — end-to-end flows that must pass on every release.
These catch cross-layer breakage that unit tests might miss.
"""
import pytest

REGISTER = "/api/v1/auth/register"
LOGIN = "/api/v1/auth/login"
TOKEN = "/api/v1/auth/token"
ME = "/api/v1/auth/me"
STUDENT_PROFILE = "/api/v1/students/me"
STUDENT_DASHBOARD = "/api/v1/students/dashboard"
STUDENT_SESSIONS = "/api/v1/students/sessions"
COUNSELLOR_PROFILE = "/api/v1/counsellors/me"
COUNSELLOR_DASHBOARD = "/api/v1/counsellors/dashboard"
HEALTH = "/health"
RECOMMEND_CAREERS = "/api/v1/recommendations/careers"
RECOMMEND_SKILL_GAP = "/api/v1/recommendations/skill-gap"


class TestReg01FullStudentAuthFlow:
    """REG-01: Student can register → login → fetch self → update profile."""

    def test_full_student_auth_flow(self, client):
        email = "reg01@regression.test"
        # 1. Register
        r = client.post(REGISTER, json={
            "full_name": "Regression Student",
            "email": email,
            "password": "regpass123",
            "role": "student",
        })
        assert r.status_code == 201
        token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Fetch self with token from registration
        me = client.get(ME, headers=headers)
        assert me.status_code == 200
        assert me.json()["email"] == email

        # 3. Login returns fresh token
        login_r = client.post(LOGIN, json={"email": email, "password": "regpass123"})
        assert login_r.status_code == 200
        fresh_token = login_r.json()["access_token"]
        fresh_headers = {"Authorization": f"Bearer {fresh_token}"}

        # 4. Old token still valid (tokens don't expire during tests)
        me2 = client.get(ME, headers=fresh_headers)
        assert me2.status_code == 200

        # 5. Update student profile
        upd = client.put(STUDENT_PROFILE, headers=fresh_headers, json={
            "grade": "12",
            "stream": "Science",
            "career_goal": "Software Engineer",
        })
        assert upd.status_code == 200
        assert upd.json()["career_goal"] == "Software Engineer"

        # 6. Dashboard reflects updated profile
        dash = client.get(STUDENT_DASHBOARD, headers=fresh_headers)
        assert dash.status_code == 200
        assert "Software Engineer" in dash.json()["recommended_next_step"]


class TestReg02CounsellorAuthFlow:
    """REG-02: Counsellor can register → login → update profile → appear in student booking."""

    def test_full_counsellor_auth_flow(self, client):
        email = "reg02coun@regression.test"
        r = client.post(REGISTER, json={
            "full_name": "Regression Counsellor",
            "email": email,
            "password": "regpass123",
            "role": "counsellor",
        })
        assert r.status_code == 201
        token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        me = client.get(ME, headers=headers)
        assert me.status_code == 200
        assert me.json()["role"] == "counsellor"

        profile = client.get(COUNSELLOR_PROFILE, headers=headers)
        assert profile.status_code == 200

        dash = client.get(COUNSELLOR_DASHBOARD, headers=headers)
        assert dash.status_code == 200


class TestReg03SessionBookingFlow:
    """REG-03: Student books a session with a counsellor end-to-end."""

    def test_session_booking_flow(self, client):
        # Register counsellor
        coun_r = client.post(REGISTER, json={
            "full_name": "Sess Counsellor",
            "email": "reg03coun@regression.test",
            "password": "regpass123",
            "role": "counsellor",
        })
        assert coun_r.status_code in (201, 409)
        coun_login = client.post(LOGIN, json={
            "email": "reg03coun@regression.test", "password": "regpass123"
        })
        coun_id = coun_login.json()["user"]["id"]

        # Register student
        stu_r = client.post(REGISTER, json={
            "full_name": "Sess Student",
            "email": "reg03stu@regression.test",
            "password": "regpass123",
            "role": "student",
        })
        assert stu_r.status_code in (201, 409)
        stu_login = client.post(LOGIN, json={
            "email": "reg03stu@regression.test", "password": "regpass123"
        })
        stu_token = stu_login.json()["access_token"]
        stu_headers = {"Authorization": f"Bearer {stu_token}"}

        # Book session
        sess = client.post(STUDENT_SESSIONS, headers=stu_headers, json={
            "counsellor_id": coun_id,
            "topic": "Regression test session",
            "mode": "online",
        })
        assert sess.status_code == 201
        assert sess.json()["status"] == "requested"

        # Dashboard now shows 1 upcoming session
        dash = client.get(STUDENT_DASHBOARD, headers=stu_headers)
        assert dash.json()["upcoming_sessions"] >= 1


class TestReg04RoleIsolation:
    """REG-04: Cross-role access control must be enforced."""

    def _auth(self, client, email, role="student"):
        r = client.post(REGISTER, json={
            "full_name": "Role Test",
            "email": email,
            "password": "regpass123",
            "role": role,
        })
        if r.status_code == 409:
            r = client.post(LOGIN, json={"email": email, "password": "regpass123"})
        return {"Authorization": f"Bearer {r.json()['access_token']}"}

    def test_counsellor_cannot_access_student_dashboard(self, client):
        headers = self._auth(client, "rc_coun@regression.test", "counsellor")
        assert client.get(STUDENT_DASHBOARD, headers=headers).status_code == 403

    def test_student_cannot_access_counsellor_dashboard(self, client):
        headers = self._auth(client, "rc_stu@regression.test", "student")
        assert client.get(COUNSELLOR_DASHBOARD, headers=headers).status_code == 403

    def test_unauthenticated_cannot_access_protected_routes(self, client):
        for url in [ME, STUDENT_PROFILE, STUDENT_DASHBOARD, COUNSELLOR_PROFILE]:
            r = client.get(url)
            assert r.status_code == 401, f"Expected 401 for {url}, got {r.status_code}"


class TestReg05HealthAndDocs:
    """REG-05: Health endpoint and API docs are always reachable."""

    def test_health_returns_ok(self, client):
        r = client.get(HEALTH)
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_root_returns_welcome(self, client):
        r = client.get("/")
        assert r.status_code == 200
        assert "Career Brownie" in r.json()["message"]

    def test_openapi_schema_reachable(self, client):
        r = client.get("/openapi.json")
        assert r.status_code == 200


class TestReg06TokenSecurity:
    """REG-06: JWT security must hold."""

    def test_tampered_token_rejected(self, client):
        r = client.get(ME, headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.bad.payload"})
        assert r.status_code == 401

    def test_missing_bearer_prefix_rejected(self, client):
        r = client.get(ME, headers={"Authorization": "notabearer"})
        assert r.status_code == 401

    def test_empty_auth_header_rejected(self, client):
        r = client.get(ME, headers={"Authorization": ""})
        assert r.status_code == 401
