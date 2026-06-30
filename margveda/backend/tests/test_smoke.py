import os

os.environ["DATABASE_URL"] = "sqlite:///./careerbrownie-test.db"

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_auth_flow():
    payload = {
        "full_name": "Smoke Test Student",
        "email": "smoke-test-student@example.com",
        "password": "strongpass123",
        "role": "student",
    }
    register_response = client.post("/api/v1/auth/register", json=payload)
    assert register_response.status_code in {201, 409}

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == payload["email"]
