from services.energy_service import EnergyService
from services.maintenance_service import MaintenanceService
from services.occupancy_service import OccupancyService
from services.security_service import SecurityService
from services.cost_service import CostService


class FacilityIntelligenceEngine:
    """
    Aggregates insights from all 5 agents and computes a single
    Facility Health Score (0-100) using a transparent, rule-based
    weighted formula — NOT a trained ML model. Weights are documented
    here so they can be explained or adjusted later.
    """

    # Weights must sum to 1.0
    WEIGHTS = {
        "maintenance": 0.30,
        "security": 0.25,
        "cost": 0.20,
        "occupancy": 0.15,
        "energy": 0.10,
    }

    def __init__(self):
        self.energy_service = EnergyService()
        self.maintenance_service = MaintenanceService()
        self.occupancy_service = OccupancyService()
        self.security_service = SecurityService()
        self.cost_service = CostService()

    def _safe_call(self, func):
        """Prevents one broken agent from crashing the whole engine."""
        try:
            return func()
        except Exception as e:
            return {"status": "error", "message": str(e), "summary": {}}

    def _score_maintenance(self, summary: dict) -> float:
        # average_health_score is already 0-100
        return float(summary.get("average_health_score", 0))

    def _score_security(self, summary: dict) -> float:
        total_events = summary.get("total_events", 0)
        unauthorized = summary.get("unauthorized_attempts", 0)

        if total_events == 0:
            return 0.0

        return round(100 - (unauthorized / total_events * 100), 2)

    def _score_cost(self, summary: dict) -> float:
        total_reports = summary.get("total_reports", 0)
        over_budget = summary.get("over_budget_reports", 0)

        if total_reports == 0:
            return 0.0

        return round(100 - (over_budget / total_reports * 100), 2)

    def _score_occupancy(self, summary: dict) -> float:
        # NOTE: occupancy dataset is a single-room sensor sample,
        # not a full multi-building feed. Treated as a proxy signal,
        # capped at 100. Higher occupancy = better space utilization.
        rate = summary.get("occupancy_rate_pct", 0)
        return round(min(rate, 100), 2)

    def _score_energy(self) -> float:
        # PLACEHOLDER: real energy savings/cost-efficiency formulas
        # are not yet defined (flagged earlier as an open item).
        # Flat neutral score used until that logic exists.
        return 70.0

    def get_facility_overview(self):

        energy = self._safe_call(self.energy_service.get_summary)
        maintenance = self._safe_call(self.maintenance_service.get_summary)
        occupancy = self._safe_call(self.occupancy_service.get_summary)
        security = self._safe_call(self.security_service.get_summary)
        cost = self._safe_call(self.cost_service.get_summary)

        scores = {
            "maintenance": self._score_maintenance(maintenance.get("summary", {})),
            "security": self._score_security(security.get("summary", {})),
            "cost": self._score_cost(cost.get("summary", {})),
            "occupancy": self._score_occupancy(occupancy.get("summary", {})),
            "energy": self._score_energy(),
        }

        facility_health_score = round(
            sum(scores[agent] * self.WEIGHTS[agent] for agent in scores),
            2
        )

        return {
            "status": "success",
            "facility_health_score": facility_health_score,
            "score_breakdown": scores,
            "score_weights": self.WEIGHTS,
            "agents": {
                "energy": energy,
                "maintenance": maintenance,
                "occupancy": occupancy,
                "security": security,
                "cost": cost,
            }
        }