import audioop
import base64


def mulaw_to_pcm(mulaw_data: bytes) -> bytes:
    return audioop.ulaw2lin(mulaw_data, 2)


def pcm_to_mulaw(pcm_data: bytes) -> bytes:
    return audioop.lin2ulaw(pcm_data, 2)


def encode_for_twilio(audio_data: bytes) -> str:
    return base64.b64encode(audio_data).decode('utf-8')


class AudioBuffer:
    def __init__(self, chunk_size: int = 8000) -> None:
        self.buffer = bytearray()
        self.chunk_size = chunk_size
    
    def add(self, chunk: bytes) -> bytes | None:
        self.buffer.extend(chunk)
        if len(self.buffer) >= self.chunk_size:
            data = bytes(self.buffer[:self.chunk_size])
            self.buffer = self.buffer[self.chunk_size:]
            return data
        return None
    
    def clear(self) -> None:
        self.buffer.clear()
