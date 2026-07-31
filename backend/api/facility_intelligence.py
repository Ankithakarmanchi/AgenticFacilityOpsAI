from fastapi import APIRouter
from core.facility_intelligence_engine import FacilityIntelligenceEngine

router = APIRouter(prefix="/api/facility-intelligence", tags=["Facility Intelligence"])
engine = FacilityIntelligenceEngine()


@router.get("/")
def get_facility_overview():
    return engine.get_facility_overview()