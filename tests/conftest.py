import pytest
from fastapi.testclient import TestClient
from voiceflow.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_redis():
    from unittest.mock import AsyncMock
    return AsyncMock()


@pytest.fixture
def mock_twilio_client():
    from unittest.mock import MagicMock
    return MagicMock()


@pytest.fixture
def mock_openai_client():
    from unittest.mock import AsyncMock
    return AsyncMock()


@pytest.fixture
def sample_audio_data():
    return b'\x00' * 8000
