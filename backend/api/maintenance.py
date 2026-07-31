from fastapi import APIRouter

from services.maintenance_service import MaintenanceService

router = APIRouter(
    prefix="/api/maintenance",
    tags=["Maintenance"]
)

maintenance_service = MaintenanceService()


@router.get("/")
def get_maintenance_summary():
    return maintenance_service.get_summary()


@router.get("/alerts")
def get_maintenance_alerts():
    return maintenance_service.get_alerts()


@router.get("/recommendations")
def get_maintenance_recommendations():
    return maintenance_service.get_recommendations()