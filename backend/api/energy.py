from fastapi import APIRouter

from services.energy_service import EnergyService

router = APIRouter(
    prefix="/api/energy",
    tags=["Energy"]
)

energy_service = EnergyService()


@router.get("/")
def get_energy_data():
    return energy_service.get_summary()


@router.get("/anomalies")
def get_energy_anomalies():
    return energy_service.get_anomalies()
@router.get("/recommendations")
def get_energy_recommendations():
    return energy_service.get_recommendations()
@router.get("/anomaly-detection")
def get_energy_anomaly_detection():
    return energy_service.get_anomaly_detection()