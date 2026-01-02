# API Reference

## Overview

Complete API reference for VoiceFlow AI endpoints, request/response formats, and error handling.

**Base URL**: `http://localhost:8000` (development) or `https://your-domain.com` (production)

---

## Authentication

Currently, API endpoints are open for development. For production, implement API key authentication:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://your-domain.com/api/calls/outbound
```

---

## Webhooks

### Incoming Call Handler

Handle incoming Twilio calls and initiate media stream.

**Endpoint**: `POST /webhook/voice/incoming`

**Request** (from Twilio):
```
Content-Type: application/x-www-form-urlencoded

CallSid=CA1234567890abcdef
From=+1234567890
To=+0987654321
CallStatus=ringing
```

**Response**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <Stream url="wss://your-domain.com/webhook/ws/media-stream/CA1234567890abcdef"/>
  </Connect>
</Response>
```

### Call Status Callback

Receive call status updates from Twilio.

**Endpoint**: `POST /webhook/voice/status`

**Request**:
```
CallSid=CA1234567890abcdef
CallStatus=completed
CallDuration=120
```

**Response**:
```json
{
  "status": "received"
}
```

### Media Stream WebSocket

Bidirectional audio streaming for real-time conversation.

**Endpoint**: `WS /webhook/ws/media-stream/{call_sid}`

**Messages from Twilio**:
```json
{
  "event": "media",
  "media": {
    "payload": "base64_encoded_audio"
  }
}
```

**Messages to Twilio**:
```json
{
  "event": "media",
  "media": {
    "payload": "base64_encoded_audio"
  }
}
```

---

## Call Management

### Initiate Outbound Call

Start an outbound call to a phone number.

**Endpoint**: `POST /api/calls/outbound`

**Request**:
```json
{
  "to_number": "+1234567890",
  "initial_message": "Hello from VoiceFlow AI"
}
```

**Response** (200 OK):
```json
{
  "call_sid": "CA1234567890abcdef",
  "status": "initiated",
  "to": "+1234567890"
}
```

**Error Response** (500):
```json
{
  "detail": "Failed to initiate call: error message"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/api/calls/outbound \
  -H "Content-Type: application/json" \
  -d '{
    "to_number": "+1234567890",
    "initial_message": "Hello!"
  }'
```

### Get Call Details

Retrieve information about a specific call.

**Endpoint**: `GET /api/calls/{call_sid}`

**Parameters**:
- `call_sid` (path): Twilio call SID

**Response** (200 OK):
```json
{
  "call_sid": "CA1234567890abcdef",
  "status": "completed",
  "duration": 120,
  "from": "+1234567890",
  "to": "+0987654321"
}
```

**Error Response** (404):
```json
{
  "detail": "Call not found"
}
```

**Example**:
```bash
curl http://localhost:8000/api/calls/CA1234567890abcdef
```

---

## Health Checks

### Basic Health Check

Simple health check endpoint.

**Endpoint**: `GET /health/`

**Response** (200 OK):
```json
{
  "status": "healthy",
  "service": "VoiceFlow AI"
}
```

**Example**:
```bash
curl http://localhost:8000/health/
```

### Detailed Health Check

Comprehensive health check with version and environment info.

**Endpoint**: `GET /health/detailed`

**Response** (200 OK):
```json
{
  "status": "healthy",
  "service": "VoiceFlow AI",
  "version": "1.0.0",
  "environment": "production"
}
```

**Example**:
```bash
curl http://localhost:8000/health/detailed
```

---

## Root Endpoint

### Service Information

Get basic service information.

**Endpoint**: `GET /`

**Response** (200 OK):
```json
{
  "status": "healthy",
  "service": "VoiceFlow AI"
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Missing or invalid authentication |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error occurred |

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Rate Limiting

**Current**: No rate limiting implemented

**Recommended for Production**:
- 100 requests per minute per IP
- 1000 requests per hour per API key
- Implement using Redis + middleware

---

## Webhooks Security

### Twilio Signature Validation

Verify webhook requests are from Twilio:

```python
from voiceflow.utils.validators import validate_twilio_signature

@router.post("/webhook/voice/incoming")
async def incoming_call(request: Request):
    if not validate_twilio_signature(request, settings.twilio_auth_token):
        raise HTTPException(status_code=401, detail="Invalid signature")
    # Process request
```

---

## Data Models

### Call

```python
{
  "id": "string",
  "direction": "inbound" | "outbound",
  "from_number": "string",
  "to_number": "string",
  "status": "initiated" | "ringing" | "in_progress" | "completed" | "failed",
  "duration": "integer",
  "created_at": "datetime",
  "completed_at": "datetime"
}
```

### Conversation Context

```python
{
  "phone_number": "string",
  "customer_name": "string",
  "account_id": "string",
  "intent": "billing" | "support" | "appointment" | "info" | "escalate" | "order",
  "metadata": {}
}
```

---

## WebSocket Protocol

### Connection

```javascript
const ws = new WebSocket('wss://your-domain.com/webhook/ws/media-stream/CALL_SID');

ws.onopen = () => {
  console.log('Connected');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

### Message Types

**Incoming Audio**:
```json
{
  "event": "media",
  "media": {
    "payload": "base64_audio_data"
  }
}
```

**Stop Event**:
```json
{
  "event": "stop"
}
```

---

## Examples

### Python Client

```python
import httpx
import asyncio

async def make_call():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/calls/outbound",
            json={
                "to_number": "+1234567890",
                "initial_message": "Hello!"
            }
        )
        return response.json()

result = asyncio.run(make_call())
print(result)
```

### JavaScript Client

```javascript
async function makeCall() {
  const response = await fetch('http://localhost:8000/api/calls/outbound', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      to_number: '+1234567890',
      initial_message: 'Hello!'
    })
  });
  
  return await response.json();
}
```

### cURL Examples

```bash
# Make outbound call
curl -X POST http://localhost:8000/api/calls/outbound \
  -H "Content-Type: application/json" \
  -d '{"to_number": "+1234567890", "initial_message": "Hello!"}'

# Get call details
curl http://localhost:8000/api/calls/CA1234567890abcdef

# Health check
curl http://localhost:8000/health/
```

---

## OpenAPI Documentation

Interactive API documentation available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## Support

For API questions: api@voiceflow-ai.com
