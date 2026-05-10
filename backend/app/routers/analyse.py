from fastapi import APIRouter, HTTPException
from httpx import HTTPError

from app.models.schemas import AnalyseRequest, AnalyseResponse
from app.services.hibp import check_pwned_password

router = APIRouter()


@router.post("/api/analyse", response_model=AnalyseResponse)
async def analyse_password(request: AnalyseRequest) -> AnalyseResponse:
    try:
        is_breached, breach_count = await check_pwned_password(request.hashPrefix)
    except HTTPError as error:
        raise HTTPException(status_code=502, detail="HIBP lookup failed") from error

    return AnalyseResponse(isBreached=is_breached, breachCount=breach_count)
