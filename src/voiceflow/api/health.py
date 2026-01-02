from fastapi import APIRouter
from voiceflow.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/")
async def health_check() -> dict:
    return {
        "status": "healthy",
        "service": "VoiceFlow AI"
    }


@router.get("/detailed")
async def detailed_health() -> dict:
    return {
        "status": "healthy",
        "service": "VoiceFlow AI",
        "version": "1.0.0",
        "environment": settings.app_env
    }
