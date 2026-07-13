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