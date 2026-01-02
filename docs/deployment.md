# Deployment Guide

## Overview

This guide covers deploying VoiceFlow AI to production environments including Docker, AWS, and other cloud platforms.

---

## Prerequisites

- Docker and Docker Compose installed
- Cloud provider account (AWS, GCP, or Azure)
- Domain name with SSL certificate
- All required API keys configured

---

## Local Development

### Using Docker Compose

```bash
# Start all services
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose -f docker/docker-compose.yml logs -f app

# Stop services
docker-compose -f docker/docker-compose.yml down
```

### Using Poetry

```bash
# Install dependencies
poetry install

# Run application
poetry run python -m voiceflow.main

# Run with auto-reload
poetry run uvicorn voiceflow.main:app --reload
```

---

## Production Deployment

### Docker Production Build

```bash
# Build production image
docker build -t voiceflow-ai:latest -f docker/Dockerfile .

# Tag for registry
docker tag voiceflow-ai:latest your-registry/voiceflow-ai:latest

# Push to registry
docker push your-registry/voiceflow-ai:latest

# Run container
docker run -d \
  --name voiceflow-ai \
  -p 8000:8000 \
  --env-file .env \
  --restart unless-stopped \
  voiceflow-ai:latest
```

---

## AWS Deployment

### Using ECS (Elastic Container Service)

**1. Push Image to ECR**

```bash
# Authenticate to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# Create repository
aws ecr create-repository --repository-name voiceflow-ai

# Tag and push
docker tag voiceflow-ai:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/voiceflow-ai:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/voiceflow-ai:latest
```

**2. Create ECS Task Definition**

```json
{
  "family": "voiceflow-ai",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "voiceflow-ai",
      "image": "YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/voiceflow-ai:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "APP_ENV", "value": "production"}
      ],
      "secrets": [
        {"name": "TWILIO_ACCOUNT_SID", "valueFrom": "arn:aws:secretsmanager:..."},
        {"name": "ANTHROPIC_API_KEY", "valueFrom": "arn:aws:secretsmanager:..."}
      ]
    }
  ]
}
```

**3. Create ECS Service**

```bash
aws ecs create-service \
  --cluster voiceflow-cluster \
  --service-name voiceflow-ai \
  --task-definition voiceflow-ai \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

**4. Configure Application Load Balancer**

- Create ALB with HTTPS listener
- Configure target group pointing to ECS service
- Enable sticky sessions for WebSocket support
- Set health check path to `/health/`

---

## Environment Configuration

### Production Environment Variables

```env
# Application
APP_ENV=production
APP_PORT=8000
LOG_LEVEL=INFO

# Twilio
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_PHONE_NUMBER=+1234567890

# AI Services
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
ELEVENLABS_API_KEY=xxxxx
ELEVENLABS_VOICE_ID=xxxxx

# Database (use managed services)
REDIS_URL=redis://production-redis.cache.amazonaws.com:6379/0
DATABASE_URL=postgresql://user:pass@production-db.rds.amazonaws.com:5432/voiceflow
```

### Using AWS Secrets Manager

```bash
# Store secrets
aws secretsmanager create-secret \
  --name voiceflow/twilio-sid \
  --secret-string "ACxxxxx"

# Reference in ECS task definition
"secrets": [
  {
    "name": "TWILIO_ACCOUNT_SID",
    "valueFrom": "arn:aws:secretsmanager:region:account:secret:voiceflow/twilio-sid"
  }
]
```

---

## Database Setup

### PostgreSQL (Production)

```bash
# Using AWS RDS
aws rds create-db-instance \
  --db-instance-identifier voiceflow-db \
  --db-instance-class db.t3.medium \
  --engine postgres \
  --master-username voiceflow \
  --master-user-password YOUR_PASSWORD \
  --allocated-storage 20

# Run migrations
poetry run alembic upgrade head
```

### Redis (Production)

```bash
# Using AWS ElastiCache
aws elasticache create-cache-cluster \
  --cache-cluster-id voiceflow-redis \
  --cache-node-type cache.t3.medium \
  --engine redis \
  --num-cache-nodes 1
```

---

## SSL/TLS Configuration

### Using Let's Encrypt

```bash
# Install certbot
sudo apt-get install certbot

# Obtain certificate
sudo certbot certonly --standalone -d voiceflow.yourdomain.com

# Configure in nginx or ALB
```

---

## Monitoring & Logging

### CloudWatch Logs

```bash
# Configure log driver in ECS task definition
"logConfiguration": {
  "logDriver": "awslogs",
  "options": {
    "awslogs-group": "/ecs/voiceflow-ai",
    "awslogs-region": "us-east-1",
    "awslogs-stream-prefix": "ecs"
  }
}
```

### Health Checks

```bash
# Configure ALB health check
Target: /health/
Interval: 30 seconds
Timeout: 5 seconds
Healthy threshold: 2
Unhealthy threshold: 3
```

---

## Scaling

### Auto-scaling Configuration

```bash
# Create auto-scaling target
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/voiceflow-cluster/voiceflow-ai \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 2 \
  --max-capacity 10

# Create scaling policy
aws application-autoscaling put-scaling-policy \
  --policy-name cpu-scaling \
  --service-namespace ecs \
  --resource-id service/voiceflow-cluster/voiceflow-ai \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration file://scaling-policy.json
```

---

## Twilio Configuration

### Production Webhook Setup

1. Go to [Twilio Console](https://console.twilio.com)
2. Navigate to Phone Numbers → Your Number
3. Set webhook URL to: `https://voiceflow.yourdomain.com/webhook/voice/incoming`
4. Enable "Primary Handler Fails" fallback URL
5. Configure status callback URL

---

## Backup & Recovery

### Database Backups

```bash
# Automated RDS backups
aws rds modify-db-instance \
  --db-instance-identifier voiceflow-db \
  --backup-retention-period 7 \
  --preferred-backup-window "03:00-04:00"

# Manual snapshot
aws rds create-db-snapshot \
  --db-instance-identifier voiceflow-db \
  --db-snapshot-identifier voiceflow-backup-$(date +%Y%m%d)
```

### Redis Backups

```bash
# Enable automatic backups in ElastiCache
aws elasticache modify-cache-cluster \
  --cache-cluster-id voiceflow-redis \
  --snapshot-retention-limit 7
```

---

## Troubleshooting

### Common Issues

**WebSocket Connection Failures**
- Ensure ALB has sticky sessions enabled
- Check security group allows WebSocket traffic
- Verify timeout settings (increase to 300s)

**High Latency**
- Check Redis connection pool settings
- Monitor API rate limits (Whisper, Claude, ElevenLabs)
- Review CloudWatch metrics for bottlenecks

**Memory Issues**
- Increase ECS task memory allocation
- Monitor audio buffer sizes
- Check for memory leaks in logs

---

## Security Checklist

- [ ] All API keys stored in secrets manager
- [ ] HTTPS enabled with valid SSL certificate
- [ ] Security groups restrict access appropriately
- [ ] Database not publicly accessible
- [ ] Regular security updates applied
- [ ] Twilio webhook signature validation enabled
- [ ] Rate limiting configured
- [ ] Logging excludes sensitive data

---

## Cost Optimization

- Use spot instances for non-critical workloads
- Enable auto-scaling to match demand
- Cache TTS responses in Redis
- Use reserved instances for predictable load
- Monitor API usage and set budgets
- Implement request throttling

---

## Support

For deployment issues, contact: devops@voiceflow-ai.com
