from fastapi import APIRouter
from services.ticket_service import TicketService

router = APIRouter(prefix="/api/tickets", tags=["Tickets"])
ticket_service = TicketService()


@router.post("/generate")
def generate_tickets():
    return ticket_service.generate_tickets_from_maintenance_alerts()


@router.get("/")
def get_tickets():
    return ticket_service.get_tickets()


@router.patch("/{ticket_id}/status")
def update_ticket_status(ticket_id: str, new_status: str):
    return ticket_service.update_ticket_status(ticket_id, new_status)


@router.post("/escalate-check")
def run_escalation_check(hours_threshold: float = 1):
    return ticket_service.run_escalation_check(hours_threshold)