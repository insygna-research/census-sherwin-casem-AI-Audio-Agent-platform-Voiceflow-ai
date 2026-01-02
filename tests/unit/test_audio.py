import pytest
from voiceflow.utils.audio import mulaw_to_pcm, pcm_to_mulaw, AudioBuffer


def test_mulaw_to_pcm_conversion():
    mulaw_data = b'\xff\x00\x80'
    pcm_data = mulaw_to_pcm(mulaw_data)
    assert isinstance(pcm_data, bytes)
    assert len(pcm_data) > 0


def test_pcm_to_mulaw_conversion():
    pcm_data = b'\x00\x00\xff\xff'
    mulaw_data = pcm_to_mulaw(pcm_data)
    assert isinstance(mulaw_data, bytes)
    assert len(mulaw_data) > 0


def test_audio_buffer_add():
    buffer = AudioBuffer(chunk_size=100)
    result = buffer.add(b'\x00' * 50)
    assert result is None
    
    result = buffer.add(b'\x00' * 60)
    assert result is not None
    assert len(result) == 100


def test_audio_buffer_clear():
    buffer = AudioBuffer()
    buffer.add(b'\x00' * 100)
    buffer.clear()
    assert len(buffer.buffer) == 0
