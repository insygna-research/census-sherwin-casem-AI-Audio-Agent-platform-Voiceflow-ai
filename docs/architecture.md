# VoiceFlow AI - Architecture Documentation

## Overview

VoiceFlow AI is an intelligent voice-based communication system that handles both inbound and outbound calls with natural language understanding, contextual memory, and seamless human escalation capabilities.

## System Architecture

### High-Level Component Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     Phone Network (PSTN)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Twilio Voice API                            │
│  • Inbound call handling                                     │
│  • Outbound call initiation                                  │
│  • Media Streams (WebSocket for real-time audio)            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Application Server                      │
│  • WebSocket handler for media streams                       │
│  • REST endpoints for webhooks                               │
│  • Async request processing                                  │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌──────────┐
   │  STT    │  │   LLM   │  │   TTS    │
   │ Engine  │  │ Engine  │  │  Engine  │
   └─────────┘  └─────────┘  └──────────┘
        │            │            │
        └────────────┼────────────┘
                     ▼
        ┌────────────────────────┐
        │  Conversation Manager   │
        │  • Intent detection     │
        │  • Context management   │
        │  • State machine        │
        └────────────┬────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌──────────┐
   │  Redis  │  │Business │  │   CRM    │
   │ Memory  │  │  Logic  │  │   API    │
   └─────────┘  └─────────┘  └──────────┘
```

## Core Components

### 1. Telephony Layer - Twilio Voice

**Purpose**: Handle phone calls and real-time audio streaming

**Key Features**:
- Inbound call webhooks
- Outbound call initiation via REST API
- Media Streams for bidirectional audio via WebSocket
- Call recording and monitoring
- Number provisioning and management

**Technology**: Twilio Voice API + Media Streams

**Integration Points**:
- Webhook endpoints for call events
- WebSocket connections for real-time audio
- REST API for programmatic call control

### 2. Application Server - FastAPI

**Purpose**: Core application logic and request orchestration

**Why FastAPI**:
- Native async/await support for handling concurrent calls
- WebSocket support for real-time media streaming
- Automatic API documentation with OpenAPI
- High performance (built on Starlette/Uvicorn)
- Type safety with Pydantic models

**Key Endpoints**:
```python
POST /webhook/voice/incoming    # Handle incoming calls
POST /webhook/voice/status      # Track call status
WS   /ws/media-stream           # Real-time audio stream
POST /api/outbound/call         # Initiate outbound calls
GET  /api/calls/history         # Call history and analytics
```

### 3. Speech-to-Text (STT) Engine

**Primary Option**: OpenAI Whisper API
- Industry-leading accuracy (99+ languages)
- Built-in noise reduction
- Timestamp support
- Low latency streaming option

**Alternative**: ElevenLabs Scribe v2 Realtime
- Sub-150ms latency
- Excellent for real-time conversations
- 90+ languages
- Speaker diarization

**Implementation Strategy**:
- Stream audio chunks from Twilio
- Process in real-time with minimal buffering
- Handle silence detection
- Concurrent processing for multiple calls

### 4. Large Language Model (LLM) - Intent & Response

**Primary Option**: Claude (Anthropic)
- Superior reasoning and context handling
- Function calling for tool integration
- Long context window (200K tokens)
- Natural conversation flow

**Architecture Pattern**: LangChain Integration
- **Agent**: ReAct agent with tools
- **Memory**: Redis-backed conversation history
- **Tools**: CRM lookup, appointment booking, ticket creation
- **Prompt Engineering**: System prompts for role-playing

**Intent Categories**:
```python
class Intent(Enum):
    BILLING_INQUIRY = "billing"
    TECHNICAL_SUPPORT = "support"
    APPOINTMENT_BOOKING = "appointment"
    GENERAL_INFO = "info"
    ESCALATION_REQUEST = "escalate"
    ORDER_STATUS = "order"
```

### 5. Text-to-Speech (TTS) Engine

**Primary Option**: ElevenLabs
- Most natural-sounding voices
- Emotion and tone control
- Voice cloning capabilities
- Streaming support for low latency

**Alternative**: Azure TTS
- Cost-effective for high volume
- Neural voices with SSML support
- Multiple language support

**Configuration**:
```python
{
    "model": "eleven_turbo_v2_5",  # Best latency/quality balance
    "voice_id": "professional_female_1",
    "optimize_streaming_latency": 3,  # Balanced mode
    "output_format": "pcm_16000"  # Matches Twilio format
}
```

### 6. Conversation State Manager

**Purpose**: Orchestrate conversation flow and maintain context

**State Machine**:
```
INITIAL → GREETING → INTENT_DETECTION → PROCESSING → RESPONSE
    ↓         ↓            ↓               ↓           ↓
    └─────────┴────────────┴───────────────┴───────────┴→ ESCALATION
                                                        → COMPLETION
```

**State Persistence**: Redis with session TTL
- Conversation history (last 10 exchanges)
- User context (name, account info, preferences)
- Intent stack (for complex multi-step processes)
- Escalation flags and metadata

### 7. Memory Layer - Redis

**Purpose**: Fast, persistent conversation memory across sessions

**Data Structures**:

```python
# Conversation history
conversation:{call_id}:history = [
    {"role": "user", "content": "...", "timestamp": "..."},
    {"role": "assistant", "content": "...", "timestamp": "..."}
]

# User context
user:{phone_number}:context = {
    "name": "John Doe",
    "account_id": "12345",
    "last_call": "2025-01-01T10:00:00Z",
    "preferences": {...}
}

# Active call state
call:{call_id}:state = {
    "intent": "billing",
    "status": "processing",
    "data": {...}
}
```

**TTL Strategy**:
- Active calls: No expiration
- Completed calls: 24 hours
- User context: 30 days
- Analytics data: 90 days

### 8. Business Logic Layer

**Purpose**: Domain-specific operations and integrations

**Modules**:

1. **CRM Integration**
   - Customer lookup by phone number
   - Update customer records
   - Retrieve account history

2. **Appointment System**
   - Check availability
   - Book/modify/cancel appointments
   - Send confirmations

3. **Ticketing System**
   - Create support tickets
   - Query ticket status
   - Escalate issues

4. **Billing Operations**
   - Retrieve billing information
   - Process payments
   - Generate invoices

**Implementation**: Tool-based architecture using LangChain
```python
@tool
def get_customer_info(phone_number: str) -> dict:
    """Retrieve customer information from CRM"""
    return crm_client.get_customer(phone_number)

@tool
def book_appointment(customer_id: str, date: str, time: str) -> dict:
    """Book an appointment for the customer"""
    return appointment_system.create(customer_id, date, time)
```

## Data Flow

### Inbound Call Flow

1. **Call Initiation**
   - Customer dials Twilio number
   - Twilio sends webhook to `/webhook/voice/incoming`
   - FastAPI returns TwiML with Media Stream instructions

2. **Audio Streaming**
   - Twilio opens WebSocket to `/ws/media-stream`
   - Audio chunks stream bidirectionally
   - FastAPI buffers and processes audio

3. **Speech Recognition**
   - Audio chunks sent to Whisper/Scribe
   - Text transcription returned with timestamps
   - Silence detection triggers processing

4. **Intent Processing**
   - Transcribed text sent to LLM with context
   - LangChain agent analyzes intent
   - Tools executed if needed (CRM lookup, etc.)

5. **Response Generation**
   - LLM generates natural language response
   - Response sent to TTS engine
   - Audio chunks streamed back via WebSocket

6. **Continuous Loop**
   - Repeat steps 3-5 until call completion
   - Update Redis with conversation state
   - Log interactions for analytics

### Outbound Call Flow

1. **Call Trigger**
   - API request or scheduled job
   - System retrieves customer info
   - Prepares conversation context

2. **Call Initiation**
   - FastAPI calls Twilio REST API
   - Specifies Media Stream URL
   - Sets initial TTS message

3. **Connection Established**
   - Customer answers
   - System plays greeting
   - Follows inbound flow from step 2

## Scalability Considerations

### Horizontal Scaling

**Application Layer**:
- Stateless FastAPI instances behind load balancer
- WebSocket sticky sessions via consistent hashing
- Container orchestration (Docker + Kubernetes)

**Redis Layer**:
- Redis Cluster for distributed memory
- Read replicas for analytics queries
- Sentinel for automatic failover

### Performance Optimization

**Audio Processing**:
- Chunk size optimization (20ms recommended)
- Parallel processing for STT/TTS
- Connection pooling for external APIs
- Caching for common responses

**Database**:
- Redis for hot data (active conversations)
- PostgreSQL for cold data (call history, analytics)
- Background workers for non-critical writes

### Cost Optimization

**API Usage**:
- Cache TTS responses for common phrases
- Batch STT requests where possible
- Use cheaper models for simple intents
- Implement rate limiting per customer

**Infrastructure**:
- Auto-scaling based on call volume
- Spot instances for non-critical workloads
- CDN for static assets
- Compression for audio streams

## Security & Compliance

### Authentication & Authorization

- API key authentication for external calls
- JWT tokens for internal services
- Role-based access control (RBAC)
- Webhook signature validation (Twilio)

### Data Protection

- Encryption in transit (TLS 1.3)
- Encryption at rest (Redis + Database)
- PII masking in logs
- Automatic data retention policies

### Compliance

- GDPR data handling
- PCI DSS for payment data
- HIPAA considerations (if healthcare)
- Call recording consent management

## Monitoring & Observability

### Metrics

- Call volume and duration
- Response latency (STT, LLM, TTS)
- Intent detection accuracy
- Escalation rate
- API error rates

### Logging

- Structured JSON logging
- Correlation IDs across services
- Audio quality metrics
- Conversation transcripts (with consent)

### Alerting

- High error rates
- Latency spikes
- Failed external API calls
- Unusual call patterns

### Tools

- Prometheus + Grafana for metrics
- ELK Stack for log aggregation
- Sentry for error tracking
- Twilio Insights for call quality

## Technology Stack Summary

| Component | Primary Technology | Alternative |
|-----------|-------------------|-------------|
| Telephony | Twilio Voice | Vonage, Plivo |
| App Server | FastAPI | Quart, Sanic |
| STT | OpenAI Whisper | ElevenLabs Scribe |
| LLM | Claude (Anthropic) | GPT-4, Gemini |
| TTS | ElevenLabs | Azure TTS, Google TTS |
| Memory | Redis | Valkey, KeyDB |
| Database | PostgreSQL | MySQL, MongoDB |
| Queue | Redis Pub/Sub | RabbitMQ, Kafka |
| Orchestration | LangChain | Custom framework |
| Hosting | AWS/GCP | Azure, DigitalOcean |

## Deployment Architecture

### Development Environment
```
Developer Machine → ngrok → Twilio Webhook
```

### Production Environment
```
Internet → AWS ALB → ECS Fargate (FastAPI) → Redis Cluster
                                            → RDS (PostgreSQL)
                                            → External APIs
```

### CI/CD Pipeline
```
GitHub → GitHub Actions → Docker Build → ECR Push → ECS Deploy
                       → Run Tests
                       → Security Scan
```