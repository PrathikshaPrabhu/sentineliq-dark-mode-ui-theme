# AI Service — Tool-84 Dark Mode UI Theme

## Overview
Flask microservice on **port 5000**. Uses Groq LLaMA-3.3-70b for AI-powered dark mode theme analysis.
Features: Redis caching, ChromaDB domain knowledge, input sanitisation, rate limiting, security headers.

## Architecture
```
  Java Backend (8080) ──► Flask AI Service (5000)
                               │
                    ┌──────────┼──────────┐
                    │          │          │
               /describe  /recommend  /generate-report
               /health
                    │
              ┌─────┴──────┐
          Groq API      Redis Cache
        (LLaMA-3.3)    (15 min TTL)
                    │
               ChromaDB
            (10 domain docs)
```

## Tech Stack
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11 | Language |
| Flask | 3.1.0 | Web framework |
| Groq API | LLaMA-3.3-70b | AI model |
| Redis | 7 | Response cache (15 min TTL) |
| ChromaDB | 0.4.24 | Domain knowledge |
| flask-limiter | 3.5.0 | Rate limiting (30 req/min) |

## Folder Structure
```
ai-service/
├── prompts/
│   ├── describe_prompt.txt
│   ├── recommend_prompt.txt
│   └── generate_report_prompt.txt
├── routes/
│   ├── describe.py           Day 3
│   ├── recommend.py          Day 4
│   ├── generate_report.py    Day 6
│   └── health.py             Day 7
├── services/
│   ├── groq_client.py        Day 2 — retry, cache, sanitise
│   ├── cache.py              Day 7 — Redis SHA256
│   └── chroma_client.py      Day 11/12 — ChromaDB
├── tests/
│   └── test_endpoints.py     Day 8 — 8 pytest tests
├── app.py
├── Dockerfile                Day 13
├── requirements.txt
├── .env.example
├── SECURITY.md
└── README.md
```

## Prerequisites
- Python 3.11+
- Redis on localhost:6379 (optional — app works without it)
- Groq API key from https://console.groq.com (free)

## Setup
```bash
cd ai-service
pip install -r requirements.txt
cp .env.example .env        # fill in GROQ_API_KEY
python app.py
```

## Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| GROQ_API_KEY | Groq API key from console.groq.com | ✅ Yes |
| REDIS_URL | Redis URL | No (defaults to redis://localhost:6379) |
| CHROMA_DATA_PATH | ChromaDB storage path | No (defaults to ./chroma_data) |

## Docker
```bash
docker build -t ai-service .
docker run -p 5000:5000 --env-file .env ai-service
```

## API Reference

### GET /health
```json
{
  "status": "ok",
  "model": "llama-3.3-70b-versatile",
  "avg_response_time_ms": 800,
  "uptime_seconds": 120
}
```

### POST /describe
**Request:** `{ "name": "Midnight Blue", "details": "Dark sidebar with neon accents" }`

**Response:**
```json
{
  "description": "Midnight Blue is a sleek dark mode theme...",
  "tags": ["dark", "neon", "sidebar"],
  "generated_at": "2026-04-21T10:00:00+00:00"
}
```

### POST /recommend
**Request:** `{ "input_text": "Dark sidebar with poor contrast" }`

**Response:**
```json
[
  {"action_type": "color", "description": "Increase contrast to 4.5:1", "priority": "high"},
  {"action_type": "typography", "description": "Increase font to 16px", "priority": "medium"},
  {"action_type": "spacing", "description": "Apply 8px grid", "priority": "low"}
]
```

### POST /generate-report
**Request:** `{ "input_text": "Dark sidebar with #1a1a2e background" }`

**Response:**
```json
{
  "title": "Dark Mode Theme Analysis",
  "summary": "A modern dark theme with strong visual hierarchy",
  "overview": "This theme uses deep navy backgrounds...",
  "key_items": ["High contrast", "Neon accents", "Clean layout"],
  "recommendations": [...],
  "generated_at": "2026-04-21T10:00:00+00:00"
}
```

## Fallback Behaviour
All endpoints return `{ "is_fallback": true }` with safe defaults if Groq is unavailable.
**The service never returns HTTP 500 due to AI failure.**

## Running Tests
```bash
pytest tests/ -v
```
All 8 tests run without live network — Groq API is fully mocked.

## Security
See [SECURITY.md](./SECURITY.md) for full threat model, test results, and sign-off.
