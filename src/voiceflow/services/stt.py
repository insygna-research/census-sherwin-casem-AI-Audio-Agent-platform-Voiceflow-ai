from openai import AsyncOpenAI
from voiceflow.config import get_settings
from voiceflow.utils.audio import mulaw_to_pcm
from voiceflow.utils.logger import get_logger
import io

logger = get_logger(__name__)
settings = get_settings()


class STTService:
    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    async def transcribe(self, audio_data: bytes) -> str | None:
        try:
            pcm_audio = mulaw_to_pcm(audio_data)
            
            audio_file = io.BytesIO(pcm_audio)
            audio_file.name = "audio.wav"
            
            response = await self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
            )
            
            return response.text if response.text else None
            
        except Exception as e:
            logger.error(f"STT error: {e}")
            return None
