# AI Service — Tool-84 Dark Mode UI Theme

## Overview
Flask microservice running on port 5000. Uses Groq LLaMA-3.3-70b for AI-powered dark mode theme analysis. Includes Redis caching (15 min TTL) and security headers.

## Tech Stack
- Python 3.11, Flask 3.x, Groq API (LLaMA-3.3-70b), Redis, flask-limiter

## Folder Structure
```
ai-service/
├── prompts/
│   ├── describe_prompt.txt
│   ├── recommend_prompt.txt
│   └── generate_report_prompt.txt
├── routes/
│   ├── describe.py
│   ├── recommend.py
│   ├── generate_report.py
│   └── health.py
├── services/
│   ├── groq_client.py
│   └── cache.py
├── app.py
├── requirements.txt
└── .env
```

## Prerequisites
- Python 3.11+
- Redis running on localhost:6379
- Groq API key from https://console.groq.com

## Setup

```bash
cd ai-service
pip install -r requirements.txt
cp .env.example .env        # then fill in your GROQ_API_KEY
python app.py
```

## Environment Variables

| Variable      | Description                              | Default                    |
|---------------|------------------------------------------|----------------------------|
| GROQ_API_KEY  | Your Groq API key from console.groq.com  | required                   |
| REDIS_URL     | Redis connection URL                     | redis://localhost:6379     |

## API Reference

### GET /health
Returns service status, model info, and uptime.

**Response:**
```json
{
  "status": "ok",
  "model": "llama-3.3-70b-versatile",
  "avg_response_time_ms": 800,
  "uptime_seconds": 120
}
```

### POST /describe
Generates a structured description for a dark mode UI theme.

**Body:**
```json
{ "name": "Midnight Blue", "details": "Dark sidebar with neon accents" }
```

**Response:**
```json
{
  "description": "A sleek dark mode theme...",
  "tags": ["dark", "neon", "sidebar"],
  "generated_at": "2026-04-21T10:00:00+00:00"
}
```

### POST /recommend
Returns 3 actionable UI/UX recommendations.

**Body:**
```json
{ "input_text": "Dark sidebar with blue accents and poor contrast" }
```

**Response:**
```json
[
  {"action_type": "color", "description": "...", "priority": "high"},
  {"action_type": "typography", "description": "...", "priority": "medium"},
  {"action_type": "spacing", "description": "...", "priority": "low"}
]
```

### POST /generate-report
Generates a full structured AI report.

**Body:**
```json
{ "input_text": "Dark sidebar with #1a1a2e background and neon blue accents" }
```

**Response:**
```json
{
  "title": "Dark Mode Theme Analysis Report",
  "summary": "A concise one-sentence summary",
  "overview": "2-3 sentence overview...",
  "key_items": ["insight 1", "insight 2", "insight 3"],
  "recommendations": [...],
  "generated_at": "2026-04-21T10:00:00+00:00"
}
```

## Fallback Behaviour
All endpoints return `{ "is_fallback": true }` with safe defaults if Groq is unavailable — the service never returns HTTP 500 due to AI failure.

## Security Headers (Day 8)
All responses include:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security`
- `Content-Security-Policy`
