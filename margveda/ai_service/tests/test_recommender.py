"""Unit tests for AI recommender, skill gap, college predictor, and roadmap."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient
from app.main import app
from app.recommender.engine import recommend_careers
from app.models.schemas import (
    CareerRecommendationRequest, SkillGapRequest,
    CollegePredictionRequest, RoadmapRequest,
)

client = TestClient(app)


class TestCareerRecommender:
    def test_returns_up_to_5_recommendations(self):
        req = CareerRecommendationRequest(
            interests=["python", "data"],
            skills=["math"],
            academic_stream="Science",
        )
        resp = recommend_careers(req)
        assert 1 <= len(resp.recommendations) <= 5

    def test_match_score_between_0_and_1(self):
        req = CareerRecommendationRequest(interests=["coding", "ai"], skills=["python"])
        resp = recommend_careers(req)
        for rec in resp.recommendations:
            assert 0 <= rec.match_score <= 1

    def test_sorted_by_match_score_descending(self):
        req = CareerRecommendationRequest(interests=["data", "statistics"], skills=["excel"])
        resp = recommend_careers(req)
        scores = [r.match_score for r in resp.recommendations]
        assert scores == sorted(scores, reverse=True)

    def test_empty_interests_still_returns_results(self):
        req = CareerRecommendationRequest(interests=[], skills=[])
        resp = recommend_careers(req)
        assert len(resp.recommendations) > 0

    def test_known_interest_boosts_relevant_career(self):
        req = CareerRecommendationRequest(interests=["python", "ai", "machine learning"], skills=["data"])
        resp = recommend_careers(req)
        top = resp.recommendations[0].title
        assert "AI" in top or "Data" in top

    def test_recommendations_have_required_fields(self):
        req = CareerRecommendationRequest(interests=["finance"], skills=["accounts"])
        resp = recommend_careers(req)
        for rec in resp.recommendations:
            assert rec.title
            assert rec.reason
            assert isinstance(rec.skills_to_build, list)


class TestSkillGapEndpoint:
    def test_skill_gap_returns_missing_skills(self):
        r = client.post("/recommendations/skill-gap", json={
            "current_skills": ["Excel"],
            "target_career": "Data Analyst",
        })
        assert r.status_code == 200
        data = r.json()
        assert "missing_skills" in data
        assert "learning_plan" in data

    def test_skill_gap_with_no_current_skills(self):
        r = client.post("/recommendations/skill-gap", json={
            "current_skills": [],
            "target_career": "Doctor",
        })
        assert r.status_code == 200
        assert len(r.json()["missing_skills"]) > 0

    def test_skill_gap_target_career_echoed_in_response(self):
        r = client.post("/recommendations/skill-gap", json={
            "current_skills": ["Python"],
            "target_career": "AI Engineer",
        })
        assert r.json()["target_career"] == "AI Engineer"


class TestCollegePredictionEndpoint:
    def test_college_prediction_returns_list(self):
        r = client.post("/recommendations/colleges", json={
            "academic_stream": "Science",
            "score_percent": 85.0,
            "preferred_location": "Delhi",
            "budget": "medium",
        })
        assert r.status_code == 200
        assert "colleges" in r.json()
        assert isinstance(r.json()["colleges"], list)

    def test_college_prediction_score_out_of_range_422(self):
        r = client.post("/recommendations/colleges", json={
            "academic_stream": "Science",
            "score_percent": 110.0,
        })
        assert r.status_code == 422

    def test_college_prediction_negative_score_422(self):
        r = client.post("/recommendations/colleges", json={
            "academic_stream": "Commerce",
            "score_percent": -5,
        })
        assert r.status_code == 422


class TestRoadmapEndpoint:
    def test_roadmap_has_required_fields(self):
        r = client.post("/roadmaps/generate", json={
            "career_goal": "Software Engineer",
            "current_level": "beginner",
            "timeline_months": 12,
        })
        assert r.status_code == 200
        data = r.json()
        assert "title" in data
        assert "career_goal" in data
        assert "stages" in data
        assert len(data["stages"]) > 0

    def test_roadmap_stages_have_title_and_duration(self):
        r = client.post("/roadmaps/generate", json={
            "career_goal": "Doctor",
            "timeline_months": 6,
        })
        for stage in r.json()["stages"]:
            assert stage["title"]
            assert stage["duration"]

    def test_roadmap_missing_career_goal_422(self):
        r = client.post("/roadmaps/generate", json={"timeline_months": 6})
        assert r.status_code == 422


class TestAIServiceHealth:
    def test_health_check(self):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"
