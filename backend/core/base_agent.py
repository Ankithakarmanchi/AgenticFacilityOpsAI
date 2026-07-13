from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgentService(ABC):
    """
    Contract every agent service must follow.
    Ensures Energy, Maintenance, Occupancy, Security, etc.
    all return data in a shape the Facility Intelligence
    Engine (and frontend) can rely on consistently.
    """

    agent_name: str = "base"

    @abstractmethod
    def get_summary(self) -> Dict[str, Any]:
        """Return the agent's KPI summary block."""
        raise NotImplementedError

    def build_response(self, status: str, message: str, summary: dict, extra: dict | None = None) -> Dict[str, Any]:
        response = {
            "agent": self.agent_name,
            "status": status,
            "message": message,
            "summary": summary,
        }
        if extra:
            response.update(extra)
        return response