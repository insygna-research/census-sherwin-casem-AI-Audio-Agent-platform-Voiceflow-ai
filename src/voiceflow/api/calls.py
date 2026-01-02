from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from twilio.rest import Client
from voiceflow.config import get_settings
from voiceflow.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)
settings = get_settings()
twilio_client = Client(
    settings.twilio_account_sid,
    settings.twilio_auth_token
)


class OutboundCallRequest(BaseModel):
    to_number: str
    initial_message: str = "Hello from VoiceFlow AI"


@router.post("/calls/outbound")
async def initiate_call(request: OutboundCallRequest) -> dict:
    try:
        call = twilio_client.calls.create(
            to=request.to_number,
            from_=settings.twilio_phone_number,
            url=f"{settings.ngrok_url}/webhook/voice/incoming"
        )
        
        return {
            "call_sid": call.sid,
            "status": call.status,
            "to": request.to_number
        }
    except Exception as e:
        logger.error(f"Failed to initiate call: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/calls/{call_sid}")
async def get_call(call_sid: str) -> dict:
    try:
        call = twilio_client.calls(call_sid).fetch()
        return {
            "call_sid": call.sid,
            "status": call.status,
            "duration": call.duration,
            "from": call.from_,
            "to": call.to
        }
    except Exception as e:
        logger.error(f"Failed to fetch call: {e}")
        raise HTTPException(status_code=404, detail="Call not found")
