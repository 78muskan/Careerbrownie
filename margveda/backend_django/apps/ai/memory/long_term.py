"""Long-term student memory — backed by PostgreSQL via the students app.

Loads a student's persisted profile for injection into agent context.
Future volumes will add write-back (updating goals, learning style, etc.).
"""
from __future__ import annotations

import logging

log = logging.getLogger("careerbrain.memory.long_term")


class StudentMemory:
    """Reads student profile from PostgreSQL for agent context injection."""

    def load(self, user_id: int | str) -> dict:
        """Return a flat dict of relevant student attributes."""
        try:
            from students.models import StudentProfile
            profile = StudentProfile.objects.select_related("user").filter(
                user_id=user_id
            ).first()
            if profile is None:
                return {}
            return _serialize_profile(profile)
        except Exception as exc:
            log.warning("StudentMemory.load(%s) failed: %s", user_id, exc)
            return {}

    def save(self, user_id: int | str, updates: dict) -> None:
        """Persist profile updates. Full implementation: CBES Volume 2."""
        log.debug("StudentMemory.save called for user %s — pending Volume 2", user_id)


def _serialize_profile(profile) -> dict:
    """Convert a StudentProfile ORM object to a flat context dict."""
    return {k: v for k, v in {
        "class": getattr(profile, "current_class", ""),
        "stream": getattr(profile, "stream", ""),
        "interests": getattr(profile, "interests", ""),
        "goals": getattr(profile, "career_goals", ""),
        "target_roles": getattr(profile, "target_roles", []),
        "location": getattr(profile, "city", ""),
        "skills": getattr(profile, "technical_skills", []),
    }.items() if v}
