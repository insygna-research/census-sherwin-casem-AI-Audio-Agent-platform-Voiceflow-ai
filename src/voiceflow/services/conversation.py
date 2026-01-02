from fastapi import WebSocket
import asyncio
import json
import base64
from voiceflow.services.stt import STTService
from voiceflow.services.tts import TTSService
from voiceflow.services.agent import VoiceAgent
from voiceflow.memory.redis_memory import RedisMemory
from voiceflow.utils.audio import AudioBuffer
from voiceflow.utils.logger import get_logger

logger = get_logger(__name__)


class ConversationManager:
    def __init__(self) -> None:
        self.stt = STTService()
        self.tts = TTSService()
        self.agent = VoiceAgent()
        self.memory = RedisMemory()
    
    async def handle_call(
        self,
        websocket: WebSocket,
        call_sid: str,
        phone_number: str
    ) -> None:
        audio_buffer = AudioBuffer()
        
        await self.tts.synthesize_stream(
            "Hello! I'm VoiceFlow AI. How can I help you today?",
            websocket
        )
        
        try:
            async for message in websocket.iter_text():
                data = json.loads(message)
                
                if data['event'] == 'media':
                    chunk = base64.b64decode(data['media']['payload'])
                    
                    audio_data = audio_buffer.add(chunk)
                    if audio_data:
                        transcript = await self.stt.transcribe(audio_data)
                        
                        if transcript:
                            logger.info(f"User: {transcript}")
                            
                            context = await self.memory.get_context(call_sid)
                            if not context:
                                context = {"phone_number": phone_number}
                            
                            response = await self.agent.process(transcript, context)
                            logger.info(f"AI: {response}")
                            
                            await self.memory.save_exchange(
                                call_sid, transcript, response
                            )
                            
                            await self.tts.synthesize_stream(response, websocket)
                
                elif data['event'] == 'stop':
                    logger.info("Call ended")
                    break
                    
        except Exception as e:
            logger.error(f"Conversation error: {e}")
        finally:
            await self.memory.close()
