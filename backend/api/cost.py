from fastapi import APIRouter
from services.cost_service import CostService

router = APIRouter(prefix="/api/cost", tags=["Cost"])
cost_service = CostService()


@router.get("/")
def get_cost_summary():
    return cost_service.get_summary()


@router.get("/recommendations")
def get_cost_recommendations():
    return cost_service.get_recommendations()