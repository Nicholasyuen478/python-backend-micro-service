from fastapi import APIRouter, status, Depends

from .schemas import HealthCheckResponse
from .health_service import HealthService, get_health_service

router = APIRouter()


@router.get(
    "/healthz",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheckResponse,
)
async def get_health(
    health_service: HealthService = Depends(get_health_service),
) -> HealthCheckResponse:
    health_status = await health_service.check_health()
    return HealthCheckResponse(status=health_status["status"])
