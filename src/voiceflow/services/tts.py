from elevenlabs import AsyncElevenLabs
from fastapi import WebSocket
from voiceflow.config import get_settings
from voiceflow.utils.audio import encode_for_twilio
from voiceflow.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


class TTSService:
    def __init__(self) -> None:
        self.client = AsyncElevenLabs(api_key=settings.elevenlabs_api_key)
    
    async def synthesize_stream(self, text: str, websocket: WebSocket) -> None:
        try:
            audio_stream = self.client.text_to_speech.convert(
                text=text,
                voice_id=settings.elevenlabs_voice_id,
                model_id="eleven_turbo_v2_5",
                output_format="ulaw_8000",
                optimize_streaming_latency=3
            )
            
            async for chunk in audio_stream:
                await websocket.send_json({
                    "event": "media",
                    "media": {
                        "payload": encode_for_twilio(chunk)
                    }
                })
                
        except Exception as e:
            logger.error(f"TTS error: {e}")
