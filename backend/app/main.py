import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import advise, analyse

load_dotenv()

app = FastAPI(title="AI Password Strength Checker API")

configured_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
allow_origins = [origin.strip() for origin in configured_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(analyse.router)
app.include_router(advise.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
