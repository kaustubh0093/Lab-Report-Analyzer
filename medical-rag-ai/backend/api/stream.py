from fastapi import APIRouter
from backend.models.schemas import HealthCheck

router = APIRouter()

@router.get("/health", response_model=HealthCheck)
def health_check():
    return {"status": "ok"}
