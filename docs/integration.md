# Integration Guide

## Overview

This guide covers integrating VoiceFlow AI with its core dependencies: Twilio, PostgreSQL, Redis, and AI services. All integrations are configured via environment variables in `.env`.

---

## Environment Configuration

### Complete .env Setup

```env
# Application
APP_ENV=development
APP_PORT=8000
LOG_LEVEL=INFO

# Twilio Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890

# AI Services
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
ELEVENLABS_API_KEY=your_elevenlabs_key_here
ELEVENLABS_VOICE_ID=your_voice_id_here

# Database
REDIS_URL=redis://localhost:6379/0
DATABASE_URL=postgresql://voiceflow:dev123@localhost:5432/voiceflow

# Development
NGROK_URL=https://your-subdomain.ngrok.io
```

---

## Twilio Integration

### 1. Account Setup

1. Sign up at [Twilio](https://www.twilio.com/try-twilio)
2. Get your Account SID and Auth Token from the [Console](https://console.twilio.com)
3. Purchase a phone number with Voice capabilities

### 2. Configure Environment Variables

```env
TWILIO_ACCOUNT_SID=ACxxxxx  # From Twilio Console
TWILIO_AUTH_TOKEN=xxxxx     # From Twilio Console
TWILIO_PHONE_NUMBER=+1234567890  # Your purchased number
```

### 3. Configure Webhooks

**For Development (using ngrok):**

```bash
# Start ngrok
ngrok http 8000

# Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
# Update .env
NGROK_URL=https://abc123.ngrok.io
```

**In Twilio Console:**
1. Go to Phone Numbers → Manage → Active Numbers
2. Click your phone number
3. Under "Voice Configuration":
   - **A call comes in**: Webhook
   - **URL**: `https://your-domain.com/webhook/voice/incoming`
   - **HTTP**: POST
4. Under "Status Callback URL":
   - **URL**: `https://your-domain.com/webhook/voice/status`
   - **HTTP**: POST

**For Production:**
Replace ngrok URL with your actual domain:
```env
NGROK_URL=https://voiceflow.yourdomain.com
```

### 4. Test Connection

```python
# Test Twilio credentials
from twilio.rest import Client

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
account = client.api.accounts(TWILIO_ACCOUNT_SID).fetch()
print(f"Connected to Twilio account: {account.friendly_name}")
```

---

## PostgreSQL Integration

### 1. Local Setup (Docker)

```bash
# Start PostgreSQL container
docker run -d \
  --name voiceflow-postgres \
  -e POSTGRES_DB=voiceflow \
  -e POSTGRES_USER=voiceflow \
  -e POSTGRES_PASSWORD=dev123 \
  -p 5432:5432 \
  postgres:16-alpine
```

### 2. Configure Environment Variable

```env
DATABASE_URL=postgresql://voiceflow:dev123@localhost:5432/voiceflow
```

### 3. Initialize Database

```bash
# Run database initialization script
poetry run python scripts/init_db.py
```

### 4. Production Setup

**Using AWS RDS:**

```env
DATABASE_URL=postgresql://username:password@your-db.rds.amazonaws.com:5432/voiceflow
```

**Connection Pooling:**
For production, use connection pooling:
```env
DATABASE_URL=postgresql://user:pass@host:5432/db?pool_size=20&max_overflow=0
```

---

## Redis Integration

### 1. Local Setup (Docker)

```bash
# Start Redis container
docker run -d \
  --name voiceflow-redis \
  -p 6379:6379 \
  redis:7-alpine
```

### 2. Configure Environment Variable

```env
REDIS_URL=redis://localhost:6379/0
```

### 3. Test Connection

```bash
# Test Redis connection
redis-cli ping
# Should return: PONG
```

### 4. Production Setup

**Using AWS ElastiCache:**

```env
REDIS_URL=redis://your-redis.cache.amazonaws.com:6379/0
```

**With Authentication:**
```env
REDIS_URL=redis://:password@host:6379/0
```

**Redis Cluster:**
```env
REDIS_URL=redis://node1:6379,node2:6379,node3:6379/0
```

---

## AI Services Integration

### 1. Anthropic (Claude)

1. Sign up at [Anthropic](https://www.anthropic.com/)
2. Get API key from [Console](https://console.anthropic.com/)
3. Configure:

```env
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
```

**Test:**
```python
from anthropic import Anthropic

client = Anthropic(api_key=ANTHROPIC_API_KEY)
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=100,
    messages=[{"role": "user", "content": "Hello"}]
)
print(message.content)
```

### 2. OpenAI (Whisper)

1. Sign up at [OpenAI](https://platform.openai.com/)
2. Get API key from [API Keys](https://platform.openai.com/api-keys)
3. Configure:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
```

**Test:**
```python
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)
models = client.models.list()
print("Connected to OpenAI")
```

### 3. ElevenLabs (TTS)

1. Sign up at [ElevenLabs](https://elevenlabs.io/)
2. Get API key from [Profile Settings](https://elevenlabs.io/app/settings)
3. Browse [Voice Lab](https://elevenlabs.io/voice-lab) and copy a voice ID
4. Configure:

```env
ELEVENLABS_API_KEY=your_api_key_here
ELEVENLABS_VOICE_ID=your_voice_id_here
```

**Test:**
```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
voices = client.voices.get_all()
print(f"Available voices: {len(voices.voices)}")
```

---

## Docker Compose Integration

All services can be started together using Docker Compose:

```bash
# Start all services
docker-compose -f docker/docker-compose.yml up -d

# Check status
docker-compose -f docker/docker-compose.yml ps

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Stop all services
docker-compose -f docker/docker-compose.yml down
```

The `docker-compose.yml` automatically configures:
- PostgreSQL on port 5432
- Redis on port 6379
- Application on port 8000

---

## Verification

### Test All Integrations

```bash
# 1. Check health endpoint
curl http://localhost:8000/health/

# 2. Test database connection
poetry run python -c "from voiceflow.config import get_settings; from sqlalchemy import create_engine; engine = create_engine(get_settings().database_url); print('Database OK')"

# 3. Test Redis connection
poetry run python -c "from redis import Redis; from voiceflow.config import get_settings; r = Redis.from_url(get_settings().redis_url); r.ping(); print('Redis OK')"

# 4. Make a test call
poetry run python scripts/test_call.py
```

---

## Troubleshooting

### Twilio Issues

**Webhook not receiving calls:**
- Verify ngrok is running and URL is updated in Twilio
- Check Twilio debugger for webhook errors
- Ensure application is running on port 8000

**Audio quality issues:**
- Check network latency
- Verify audio format configuration (μ-law 8kHz)
- Monitor API response times

### Database Issues

**Connection refused:**
- Verify PostgreSQL is running: `docker ps`
- Check DATABASE_URL format
- Ensure port 5432 is not blocked

**Migration errors:**
- Run: `poetry run alembic upgrade head`
- Check database permissions

### Redis Issues

**Connection timeout:**
- Verify Redis is running: `redis-cli ping`
- Check REDIS_URL format
- Ensure port 6379 is accessible

**Memory issues:**
- Monitor Redis memory: `redis-cli info memory`
- Set maxmemory policy in redis.conf

### AI Service Issues

**Rate limiting:**
- Check API usage in respective dashboards
- Implement retry logic with exponential backoff
- Monitor rate limit headers

**API errors:**
- Verify API keys are correct
- Check account status and billing
- Review API documentation for changes

---

## Production Checklist

- [ ] All API keys stored in secure secrets manager
- [ ] Database using managed service (RDS, etc.)
- [ ] Redis using managed service (ElastiCache, etc.)
- [ ] Twilio webhooks pointing to production domain
- [ ] SSL/TLS enabled for all connections
- [ ] Environment variables not committed to git
- [ ] Backup strategy configured
- [ ] Monitoring and alerting set up
- [ ] Rate limiting configured
- [ ] Health checks configured

---

## Support

For integration issues: support@voiceflow-ai.com
