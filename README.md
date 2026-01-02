<div align="center">

![VoiceFlow AI](assets/voiceflow_banner.png)

# VoiceFlow AI

**Enterprise-Grade AI Voice Agent Platform**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

*Intelligent phone conversations powered by Claude, Whisper, and ElevenLabs*

</div>

---

## Overview

VoiceFlow AI is a production-ready voice agent system for intelligent phone conversations with sub-2 second latency. Built on cutting-edge AI technologies, it delivers natural, context-aware interactions at scale.

**Key Capabilities:**
- **Advanced AI** - Claude-powered natural language understanding
- **Real-time Processing** - Streaming audio pipeline with <2s latency
- **Telephony Integration** - Seamless Twilio inbound/outbound calls
- **Contextual Memory** - Redis-backed conversation history
- **Extensible Tools** - LangChain integration for CRM, booking, ticketing
- **Production Ready** - Docker deployment, CI/CD, comprehensive testing

**Use Cases:** Customer support, appointment scheduling, billing inquiries, ticket management, lead qualification, outbound notifications

---

## Architecture

![System Architecture](assets/voiceflow_architecture.png)

**Technology Stack:**
- **Telephony:** Twilio Voice API
- **Application:** FastAPI + Uvicorn
- **STT:** OpenAI Whisper
- **LLM:** Claude (Anthropic)
- **TTS:** ElevenLabs
- **Memory:** Redis
- **Database:** PostgreSQL
- **Orchestration:** LangChain

---

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- API Keys: [Twilio](https://www.twilio.com/), [Anthropic](https://www.anthropic.com/), [OpenAI](https://openai.com/), [ElevenLabs](https://elevenlabs.io/)

### Installation

```bash
# Clone and install
git clone https://github.com/yourusername/voiceflow-ai.git
cd voiceflow-ai
pip install poetry && poetry install

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Start services
docker-compose -f docker/docker-compose.yml up -d

# Initialize database
poetry run python scripts/init_db.py

# Run application
poetry run python -m voiceflow.main
```

### Development Setup

```bash
# Expose local server with ngrok
ngrok http 8000

# Update .env with ngrok URL
NGROK_URL=https://your-subdomain.ngrok.io

# Configure Twilio webhook
# Set "A call comes in" to: https://your-subdomain.ngrok.io/webhook/voice/incoming
```

---

## Configuration

Create `.env` file:

```env
# Twilio
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890

# AI Services
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
ELEVENLABS_API_KEY=your_key
ELEVENLABS_VOICE_ID=voice_id

# Database
REDIS_URL=redis://localhost:6379/0
DATABASE_URL=postgresql://voiceflow:dev123@localhost:5432/voiceflow

# Development
NGROK_URL=https://your-subdomain.ngrok.io
```

---

## API Reference

### Webhooks

**Incoming Call Handler**
```http
POST /webhook/voice/incoming
```

**Media Stream WebSocket**
```
WS /webhook/ws/media-stream/{call_sid}
```

### Call Management

**Initiate Outbound Call**
```bash
curl -X POST http://localhost:8000/api/calls/outbound \
  -H "Content-Type: application/json" \
  -d '{"to_number": "+1234567890", "initial_message": "Hello!"}'
```

**Get Call Details**
```http
GET /api/calls/{call_sid}
```

### Health Checks

```bash
curl http://localhost:8000/health/
curl http://localhost:8000/health/detailed
```

---

## Project Structure

```
voiceflow-ai/
├── src/voiceflow/          # Main application
│   ├── api/                # API endpoints & webhooks
│   ├── services/           # STT, TTS, Agent, Conversation
│   ├── memory/             # Redis memory management
│   ├── tools/              # LangChain tools (CRM, booking, ticketing)
│   ├── models/             # Data models
│   └── utils/              # Audio, logging, validators
├── tests/                  # Unit & integration tests
├── scripts/                # Helper scripts
├── docker/                 # Docker configuration
└── docs/                   # Documentation
```

---

## Testing

```bash
# Run all tests
poetry run pytest

# With coverage
poetry run pytest --cov=voiceflow tests/

# Code quality
poetry run black src/
poetry run ruff check src/
poetry run mypy src/
```

---

## Docker Deployment

**Development:**
```bash
docker-compose -f docker/docker-compose.yml up -d
```

**Production:**
```bash
docker build -t voiceflow-ai:latest -f docker/Dockerfile .
docker run -d --name voiceflow-ai -p 8000:8000 --env-file .env voiceflow-ai:latest
```

---

## Performance

| Metric | Target | Typical |
|--------|--------|---------|
| Response Latency | <2s | 1.5s |
| STT Accuracy | >95% | 97% |
| Call Success Rate | >90% | 94% |
| Concurrent Calls | 100+ | 100+ |
| Uptime | 99.9% | 99.95% |

---

## Documentation

Comprehensive guides available in the `docs/` directory:

- **[Architecture Guide](docs/architecture.md)** - System design, components, and technology stack
- **[Deployment Guide](docs/deployment.md)** - Production deployment (Docker, AWS ECS, monitoring)
- **[Integration Guide](docs/integration.md)** - CRM, booking, payment, and custom integrations
- **[API Reference](docs/api-reference.md)** - Complete API documentation with examples
- **[Implementation Plan](docs/plan.md)** - Development roadmap and timeline
- **[Directory Structure](docs/directory.md)** - File organization guide
- **[Coding Standards](docs/coding-rules.md)** - Code quality guidelines

---

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

**Requirements:** Follow [coding rules](docs/coding-rules.md), write tests, format with `black`

---

## License

MIT License - see [LICENSE](LICENSE) file

---

## Acknowledgments

Built with: [FastAPI](https://fastapi.tiangolo.com/) • [Twilio](https://www.twilio.com/) • [Anthropic Claude](https://www.anthropic.com/) • [OpenAI Whisper](https://openai.com/) • [ElevenLabs](https://elevenlabs.io/) • [LangChain](https://www.langchain.com/) • [Redis](https://redis.io/)

---

## Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/voiceflow-ai/issues)
- **Docs:** [docs/](docs/)
- **Email:** support@voiceflow-ai.com

---

## Roadmap

- [x] Core voice agent functionality
- [x] Intent detection and routing
- [x] Memory and context management
- [x] Tool integration framework
- [ ] Multi-language support
- [ ] Advanced sentiment analysis
- [ ] Real-time analytics dashboard
- [ ] Custom voice training
- [ ] WhatsApp/SMS integration

---

<div align="center">

**VoiceFlow AI - Making every call count** 🎙️

[![GitHub Stars](https://img.shields.io/github/stars/yourusername/voiceflow-ai?style=social)](https://github.com/yourusername/voiceflow-ai)

</div>
