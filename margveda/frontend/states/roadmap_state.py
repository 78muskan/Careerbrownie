import reflex as rx

from services.api import api_client
from states.auth_state import AuthState


class RoadmapState(rx.State):
    target_career: str = "AI and Machine Learning Engineer"
    current_skills: str = "Python, Math"
    timeline_months: int = 12
    roadmap: dict = {}
    roadmap_summary: str = "No roadmap generated yet."
    roadmap_milestones: list[dict] = []
    saved_roadmaps: list[dict] = []
    is_loading: bool = False

    async def generate(self):
        auth = await self.get_state(AuthState)
        self.is_loading = True
        try:
            data = await api_client.post(
                "/roadmaps/generate",
                token=auth.token,
                json={
                    "target_career": self.target_career,
                    "current_skills": self._split(self.current_skills),
                    "timeline_months": self.timeline_months,
                },
            )
            self.roadmap = data
            self.roadmap_summary = data.get("summary", self.roadmap_summary)
            self.roadmap_milestones = data.get("milestones", [])
        finally:
            self.is_loading = False

    async def load_saved(self):
        auth = await self.get_state(AuthState)
        data = await api_client.get("/roadmaps/me", token=auth.token)
        if isinstance(data, list):
            self.saved_roadmaps = data

    def _split(self, value: str) -> list[str]:
        return [item.strip() for item in value.split(",") if item.strip()]
