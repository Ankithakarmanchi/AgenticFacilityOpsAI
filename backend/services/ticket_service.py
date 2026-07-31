import json
from pathlib import Path
from datetime import datetime

from services.maintenance_service import MaintenanceService
from core.base_agent import BaseAgentService


class TicketService(BaseAgentService):

    agent_name = "tickets"

    def __init__(self):
        self.tickets_path = Path(__file__).parent.parent / "data" / "tickets.json"
        self.maintenance_service = MaintenanceService()

        if not self.tickets_path.exists():
            self.tickets_path.write_text("[]")
    def get_summary(self):
        return self.get_tickets()

    def _load_tickets(self):
        with open(self.tickets_path, "r") as f:
            return json.load(f)

    def _save_tickets(self, tickets):
        with open(self.tickets_path, "w") as f:
            json.dump(tickets, f, indent=2, default=str)

    def _next_ticket_id(self, tickets):
        return f"TCK{len(tickets) + 1:04d}"

    def _priority_from_health_score(self, health_score):
        if health_score < 40:
            return "Critical"
        elif health_score < 55:
            return "High"
        else:
            return "Medium"

    def generate_tickets_from_maintenance_alerts(self):
        tickets = self._load_tickets()

        existing_keys = {
            (t["asset"], t["product_id"]) for t in tickets
        }

        alerts = self.maintenance_service.get_alerts()

        created_count = 0

        for alert in alerts:
            key = (alert["asset"], alert["product_id"])

            if key in existing_keys:
                continue

            priority = self._priority_from_health_score(alert["health_score"])
            now = datetime.now().isoformat()

            ticket = {
                "ticket_id": self._next_ticket_id(tickets),
                "asset": alert["asset"],
                "product_id": alert["product_id"],
                "health_score": alert["health_score"],
                "priority": priority,
                "status": "Open",
                "escalated": priority == "Critical",
                "created_at": now,
                "escalated_at": now if priority == "Critical" else None,
                "notes": alert["message"],
            }

            tickets.append(ticket)
            existing_keys.add(key)
            created_count += 1

        self._save_tickets(tickets)

        return self.build_response(
            status="success",
            message=f"{created_count} new ticket(s) created from maintenance alerts.",
            summary={
                "new_tickets_created": created_count,
                "total_tickets": len(tickets),
            }
        )

    def get_tickets(self):
        tickets = self._load_tickets()

        summary = {
            "total_tickets": len(tickets),
            "open_tickets": len([t for t in tickets if t["status"] == "Open"]),
            "in_progress_tickets": len([t for t in tickets if t["status"] == "In Progress"]),
            "resolved_tickets": len([t for t in tickets if t["status"] == "Resolved"]),
            "escalated_tickets": len([t for t in tickets if t["escalated"]]),
        }

        return self.build_response(
            status="success",
            message="Tickets retrieved successfully.",
            summary=summary,
            extra={"tickets": tickets}
        )

    def update_ticket_status(self, ticket_id, new_status):
        tickets = self._load_tickets()
        found = False

        for t in tickets:
            if t["ticket_id"] == ticket_id:
                t["status"] = new_status
                found = True
                break

        if not found:
            return self.build_response(
                status="error",
                message=f"Ticket {ticket_id} not found.",
                summary={}
            )

        self._save_tickets(tickets)

        return self.build_response(
            status="success",
            message=f"Ticket {ticket_id} updated to '{new_status}'.",
            summary={"ticket_id": ticket_id, "new_status": new_status}
        )

    def run_escalation_check(self, hours_threshold: float = 1):
        """
        NOTE: hours_threshold defaults to 1 hour for demo/testing.
        In production this would typically be 24-48 hours, run
        automatically on a schedule (e.g. APScheduler/cron) rather
        than triggered manually via an endpoint.
        """
        tickets = self._load_tickets()
        escalated_count = 0
        now = datetime.now()

        priority_order = ["Medium", "High", "Critical"]

        for t in tickets:
            if t["status"] != "Open" or t["escalated"]:
                continue

            created_at = datetime.fromisoformat(t["created_at"])
            hours_open = (now - created_at).total_seconds() / 3600

            if hours_open >= hours_threshold:
                current_index = (
                    priority_order.index(t["priority"])
                    if t["priority"] in priority_order else 0
                )
                new_index = min(current_index + 1, len(priority_order) - 1)

                t["priority"] = priority_order[new_index]
                t["escalated"] = True
                t["escalated_at"] = now.isoformat()

                escalated_count += 1

        self._save_tickets(tickets)

        return self.build_response(
            status="success",
            message=f"{escalated_count} ticket(s) escalated.",
            summary={
                "hours_threshold_used": hours_threshold,
                "tickets_escalated": escalated_count,
            }
        )