import reflex as rx

from services.api_client import api_request


class AdminState(rx.State):
    token: str = rx.LocalStorage("", name="margveda_token")
    stats: dict = {}
    total_users: int = 0
    students: int = 0
    counsellors: int = 0
    sessions: int = 0
    roadmaps: int = 0
    users: list[dict] = []
    message: str = ""

    def load_dashboard(self):
        if not self.token:
            self.message = "Please log in as an admin."
            return
        try:
            self.stats = api_request("GET", "/admin/dashboard", token=self.token)
            self.total_users = self.stats.get("total_users", 0)
            self.students = self.stats.get("students", 0)
            self.counsellors = self.stats.get("counsellors", 0)
            self.sessions = self.stats.get("sessions", 0)
            self.roadmaps = self.stats.get("roadmaps", 0)
            self.users = api_request("GET", "/admin/users", token=self.token)
        except ValueError as exc:
            self.message = str(exc)
