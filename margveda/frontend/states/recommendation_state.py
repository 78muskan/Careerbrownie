import reflex as rx

from services.api_client import api_request


def _csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


class RecommendationState(rx.State):
    token: str = rx.LocalStorage("", name="margveda_token")
    recommendations: list[dict] = []
    colleges: list[dict] = []
    skill_gap: dict = {}
    skill_target: str = ""
    missing_skills: list[str] = []
    learning_plan: list[str] = []
    roadmap: dict = {}
    roadmap_title: str = ""
    roadmap_stages: list[dict] = []
    roadmaps: list[dict] = []
    message: str = ""

    def recommend(self, form_data: dict):
        payload = {
            "interests": _csv(form_data.get("interests", "")),
            "skills": _csv(form_data.get("skills", "")),
            "academic_stream": form_data.get("academic_stream", ""),
            "preferred_location": form_data.get("preferred_location", ""),
        }
        try:
            data = api_request("POST", "/recommendations/careers", payload, token=self.token)
            self.recommendations = data.get("recommendations", [])
        except ValueError as exc:
            self.message = str(exc)

    def analyze_skill_gap(self, form_data: dict):
        payload = {
            "current_skills": _csv(form_data.get("current_skills", "")),
            "target_career": form_data.get("target_career", ""),
        }
        try:
            self.skill_gap = api_request("POST", "/recommendations/skill-gap", payload, token=self.token)
            self.skill_target = self.skill_gap.get("target_career", "")
            self.missing_skills = self.skill_gap.get("missing_skills", [])
            self.learning_plan = self.skill_gap.get("learning_plan", [])
        except ValueError as exc:
            self.message = str(exc)

    def predict_colleges(self, form_data: dict):
        payload = {
            "academic_stream": form_data.get("academic_stream", ""),
            "score_percent": float(form_data.get("score_percent") or 0),
            "preferred_location": form_data.get("preferred_location", ""),
            "budget": form_data.get("budget", ""),
        }
        try:
            data = api_request("POST", "/recommendations/colleges", payload, token=self.token)
            self.colleges = data.get("colleges", [])
        except ValueError as exc:
            self.message = str(exc)

    def generate_roadmap(self, form_data: dict):
        payload = {
            "career_goal": form_data.get("career_goal", ""),
            "current_level": form_data.get("current_level", ""),
            "timeline_months": int(form_data.get("timeline_months") or 12),
        }
        try:
            self.roadmap = api_request("POST", "/recommendations/roadmaps", payload, token=self.token)
            self.roadmap_title = self.roadmap.get("title", "")
            self.roadmap_stages = self.roadmap.get("stages", [])
            self.load_roadmaps()
        except ValueError as exc:
            self.message = str(exc)

    def load_roadmaps(self):
        if not self.token:
            return
        try:
            self.roadmaps = api_request("GET", "/recommendations/roadmaps", token=self.token)
        except ValueError as exc:
            self.message = str(exc)
