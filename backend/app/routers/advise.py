from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.schemas import AdviseRequest
from app.services.llm import stream_advice

router = APIRouter()


@router.post("/api/advise")
async def advise_password(payload: AdviseRequest) -> StreamingResponse:
    return StreamingResponse(
        stream_advice(payload),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
