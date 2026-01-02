from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from voiceflow.api import webhooks, calls, health
from voiceflow.config import get_settings
from voiceflow.utils.logger import setup_logging

settings = get_settings()
setup_logging(settings.log_level)

app = FastAPI(title="VoiceFlow AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhooks.router, prefix="/webhook", tags=["webhooks"])
app.include_router(calls.router, prefix="/api", tags=["calls"])
app.include_router(health.router, prefix="/health", tags=["health"])


@app.get("/")
async def root() -> dict:
    return {"status": "healthy", "service": "VoiceFlow AI"}


def main() -> None:
    import uvicorn
    uvicorn.run(
        "voiceflow.main:app",
        host="0.0.0.0",
        port=settings.app_port,
        reload=settings.app_env == "development"
    )


if __name__ == "__main__":
    main()
