import reflex as rx

from services.api_client import api_request


class StudentState(rx.State):
    token: str = rx.LocalStorage("", name="margveda_token")
    grade: str = ""
    stream: str = ""
    interests: str = ""
    skills: str = ""
    career_goal: str = ""
    preferred_location: str = ""
    budget: str = ""
    roadmap_count: int = 0
    upcoming_sessions: int = 0
    next_step: str = "Complete your profile."
    message: str = ""

    def load_dashboard(self):
        if not self.token:
            self.message = "Please log in first."
            return
        try:
            data = api_request("GET", "/students/dashboard", token=self.token)
            profile = data.get("profile") or {}
            self.grade = profile.get("grade") or ""
            self.stream = profile.get("stream") or ""
            self.interests = profile.get("interests") or ""
            self.skills = profile.get("skills") or ""
            self.career_goal = profile.get("career_goal") or ""
            self.preferred_location = profile.get("preferred_location") or ""
            self.budget = profile.get("budget") or ""
            self.roadmap_count = data.get("roadmap_count", 0)
            self.upcoming_sessions = data.get("upcoming_sessions", 0)
            self.next_step = data.get("recommended_next_step", "")
        except ValueError as exc:
            self.message = str(exc)

    def update_profile(self, form_data: dict):
        try:
            api_request("PUT", "/students/me", form_data, token=self.token)
            self.message = "Profile saved."
            self.load_dashboard()
        except ValueError as exc:
            self.message = str(exc)
