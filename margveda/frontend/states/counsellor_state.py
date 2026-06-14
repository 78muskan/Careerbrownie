import reflex as rx

from services.api_client import api_request


class CounsellorState(rx.State):
    token: str = rx.LocalStorage("", name="margveda_token")
    specialization: str = ""
    bio: str = ""
    availability: str = ""
    years_experience: int = 0
    total_sessions: int = 0
    requested_sessions: int = 0
    sessions: list[dict] = []
    message: str = ""

    def load_dashboard(self):
        if not self.token:
            self.message = "Please log in as a counsellor."
            return
        try:
            data = api_request("GET", "/counsellors/dashboard", token=self.token)
            profile = data.get("profile") or {}
            self.specialization = profile.get("specialization") or ""
            self.bio = profile.get("bio") or ""
            self.availability = profile.get("availability") or ""
            self.years_experience = profile.get("years_experience") or 0
            self.total_sessions = data.get("total_sessions", 0)
            self.requested_sessions = data.get("requested_sessions", 0)
            self.sessions = data.get("upcoming_sessions", [])
        except ValueError as exc:
            self.message = str(exc)

    def update_profile(self, form_data: dict):
        payload = {
            "specialization": form_data.get("specialization", ""),
            "bio": form_data.get("bio", ""),
            "availability": form_data.get("availability", ""),
            "years_experience": int(form_data.get("years_experience") or 0),
        }
        try:
            api_request("PUT", "/counsellors/me", payload, token=self.token)
            self.message = "Counsellor profile saved."
            self.load_dashboard()
        except ValueError as exc:
            self.message = str(exc)
