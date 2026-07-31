from fastapi import APIRouter
from services.occupancy_service import OccupancyService

router = APIRouter(prefix="/api/occupancy", tags=["Occupancy"])
occupancy_service = OccupancyService()


@router.get("/")
def get_occupancy_summary():
    return occupancy_service.get_summary()
@router.get("/forecast-accuracy")
def get_occupancy_forecast_accuracy():
    return occupancy_service.get_forecast_accuracy()