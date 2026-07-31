from fastapi import APIRouter
from services.security_service import SecurityService

router = APIRouter(prefix="/api/security", tags=["Security"])
security_service = SecurityService()


@router.get("/")
def get_security_summary():
    return security_service.get_summary()


@router.get("/alerts")
def get_security_alerts():
    return security_service.get_alerts()