"""Tool base class — every agent tool implements this interface.

Tools are discrete capabilities an agent can invoke:
  - WebSearchTool
  - DatabaseQueryTool
  - NotificationTool
  - CalendarTool
  - EmailTool
  ...

Full tool implementations: CBES Volumes 5–11 (per agent).
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class ToolResult:
    success: bool
    data: Any = None
    error: str = ""


class BaseTool(ABC):
    """Abstract tool that an agent can call."""

    name: str = "base_tool"
    description: str = ""

    @abstractmethod
    def run(self, **kwargs: Any) -> ToolResult: ...

    def __repr__(self) -> str:
        return f"<Tool {self.name!r}: {self.description}>"
