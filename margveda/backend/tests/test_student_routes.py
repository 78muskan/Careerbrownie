"""Integration tests for /api/v1/students/* routes."""


REGISTER_URL = "/api/v1/auth/register"
LOGIN_URL = "/api/v1/auth/login"
PROFILE_URL = "/api/v1/students/me"
DASHBOARD_URL = "/api/v1/students/dashboard"
SESSIONS_URL = "/api/v1/students/sessions"


def _setup_student(client, email="st_route@test.com"):
    client.post(REGISTER_URL, json={
        "full_name": "Route Student",
        "email": email,
        "password": "routepass1",
        "role": "student",
    })
    r = client.post(LOGIN_URL, json={"email": email, "password": "routepass1"})
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def _setup_counsellor(client, email="co_route@test.com"):
    r = client.post(REGISTER_URL, json={
        "full_name": "Route Counsellor",
        "email": email,
        "password": "routepass1",
        "role": "counsellor",
    })
    if r.status_code == 409:
        r = client.post(LOGIN_URL, json={"email": email, "password": "routepass1"})
    return r.json()["user"]["id"] if "user" in r.json() else None


class TestStudentProfileRoute:
    def test_get_profile_requires_auth(self, client):
        assert client.get(PROFILE_URL).status_code == 401

    def test_get_profile_returns_profile(self, client):
        headers = _setup_student(client, "get_prof@test.com")
        r = client.get(PROFILE_URL, headers=headers)
        assert r.status_code == 200

    def test_update_profile_persists(self, client):
        headers = _setup_student(client, "upd_prof@test.com")
        r = client.put(PROFILE_URL, headers=headers, json={
            "grade": "12",
            "stream": "Science",
            "career_goal": "IIT Engineer",
        })
        assert r.status_code == 200
        data = r.json()
        assert data["grade"] == "12"
        assert data["career_goal"] == "IIT Engineer"

    def test_update_then_get_reflects_changes(self, client):
        headers = _setup_student(client, "get_after_upd@test.com")
        client.put(PROFILE_URL, headers=headers, json={"stream": "Arts"})
        r = client.get(PROFILE_URL, headers=headers)
        assert r.json()["stream"] == "Arts"

    def test_counsellor_cannot_access_student_dashboard(self, client):
        client.post(REGISTER_URL, json={
            "full_name": "Counsellor A",
            "email": "ca@test.com",
            "password": "routepass1",
            "role": "counsellor",
        })
        login = client.post(LOGIN_URL, json={"email": "ca@test.com", "password": "routepass1"})
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
        r = client.get(DASHBOARD_URL, headers=headers)
        assert r.status_code == 403


class TestStudentDashboardRoute:
    def test_dashboard_requires_auth(self, client):
        assert client.get(DASHBOARD_URL).status_code == 401

    def test_dashboard_returns_required_keys(self, client):
        headers = _setup_student(client, "dash_test@test.com")
        r = client.get(DASHBOARD_URL, headers=headers)
        assert r.status_code == 200
        data = r.json()
        assert "profile" in data
        assert "roadmap_count" in data
        assert "upcoming_sessions" in data
        assert "recommended_next_step" in data


class TestSessionBookingRoute:
    def test_book_session_requires_student_role(self, client):
        client.post(REGISTER_URL, json={
            "full_name": "C2",
            "email": "c2@test.com",
            "password": "routepass1",
            "role": "counsellor",
        })
        login = client.post(LOGIN_URL, json={"email": "c2@test.com", "password": "routepass1"})
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
        r = client.post(SESSIONS_URL, headers=headers, json={
            "counsellor_id": 1,
            "topic": "Help me",
            "mode": "online",
        })
        assert r.status_code == 403

    def test_book_session_with_valid_counsellor(self, client):
        c_id = _setup_counsellor(client, "c3@test.com")
        headers = _setup_student(client, "s3@test.com")
        r = client.post(SESSIONS_URL, headers=headers, json={
            "counsellor_id": c_id,
            "topic": "Career advice",
            "mode": "online",
        })
        assert r.status_code == 201

    def test_book_session_invalid_counsellor_404(self, client):
        headers = _setup_student(client, "s4@test.com")
        r = client.post(SESSIONS_URL, headers=headers, json={
            "counsellor_id": 99999,
            "topic": "Test",
            "mode": "online",
        })
        assert r.status_code == 404
