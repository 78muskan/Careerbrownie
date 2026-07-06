"""Agent Registry — maps agent names to classes; bootstraps on Django ready().

Usage:
    @AgentRegistry.register("career")
    class CareerAgent(BaseAgent): ...

    registry = AgentRegistry()
    agent = registry.select("career")
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .base import BaseAgent

if TYPE_CHECKING:
    pass

log = logging.getLogger("careerbrain.registry")


class AgentRegistry:
    """Central agent registry. Populated via the @register decorator."""

    _agents: dict[str, type[BaseAgent]] = {}

    @classmethod
    def register(cls, name: str):
        """Class decorator that registers an agent under `name`."""
        def decorator(agent_cls: type[BaseAgent]) -> type[BaseAgent]:
            agent_cls.name = name
            cls._agents[name] = agent_cls
            log.debug("Registered agent: %s → %s", name, agent_cls.__name__)
            return agent_cls
        return decorator

    @classmethod
    def bootstrap(cls) -> None:
        """Import all agent modules so their @register decorators fire."""
        from apps.ai.agents.career.agent import CareerAgent  # noqa: F401
        from apps.ai.agents.crm.agent import CRMAgent        # noqa: F401
        from apps.ai.agents.booking.agent import BookingAgent  # noqa: F401
        log.info("CareerBrain: %d agents registered: %s", len(cls._agents), list(cls._agents))

    def select(self, hint: str) -> BaseAgent:
        """Return the best agent for the given routing hint."""
        if not self._agents:
            self.bootstrap()
        agent_cls = self._agents.get(hint) or self._agents.get("career")
        if agent_cls is None:
            raise RuntimeError(
                "No agents registered. Did AgentRegistry.bootstrap() run? "
                "Check apps.ai AppConfig.ready()."
            )
        return agent_cls()

    def all_names(self) -> list[str]:
        return list(self._agents.keys())
