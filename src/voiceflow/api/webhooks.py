from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Form, Response
from twilio.twiml.voice_response import VoiceResponse, Connect
from voiceflow.services.conversation import ConversationManager
from voiceflow.config import get_settings
from voiceflow.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)
settings = get_settings()
conversation_manager = ConversationManager()


@router.post("/voice/incoming")
async def incoming_call(
    CallSid: str = Form(...),
    From: str = Form(...)
) -> Response:
    logger.info(f"Incoming call from {From}, SID: {CallSid}")
    
    response = VoiceResponse()
    connect = Connect()
    stream_url = f"{settings.ngrok_url}/webhook/ws/media-stream/{CallSid}"
    connect.stream(url=stream_url)
    response.append(connect)
    
    return Response(content=str(response), media_type="application/xml")


@router.websocket("/ws/media-stream/{call_sid}")
async def media_stream(websocket: WebSocket, call_sid: str) -> None:
    await websocket.accept()
    logger.info(f"WebSocket connected: {call_sid}")
    
    phone_number = "unknown"
    
    try:
        await conversation_manager.handle_call(
            websocket, call_sid, phone_number
        )
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {call_sid}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")


@router.post("/voice/status")
async def call_status(
    CallSid: str = Form(...),
    CallStatus: str = Form(...)
) -> dict:
    logger.info(f"Call status update: {CallSid} - {CallStatus}")
    return {"status": "received"}
