# SECURITY.md — AI Service | Tool-84 Dark Mode UI Theme

## Team Sign-Off
| Member | Role | Sign-Off |
|--------|------|----------|
| AI Developer 1 | Flask setup, endpoints, ChromaDB | ✅ Signed |
| AI Developer 2 | GroqClient, security review, prompt tuning | ✅ Signed |

---

## Threat Model — 5 Threats Identified (Day 2)

### Threat 1: Prompt Injection
**Description:** Attacker embeds instructions like "ignore previous instructions" to hijack AI behaviour.
**Mitigation:** `sanitise_input()` in `groq_client.py` detects injection patterns with regex → returns HTTP 400.
**Status:** ✅ Fixed and tested.

### Threat 2: API Key Exposure
**Description:** Groq API key committed to GitHub becomes public.
**Mitigation:** Key stored only in `.env`. `.env` is in `.gitignore`. `.env.example` committed instead.
**Status:** ✅ Fixed.

### Threat 3: Rate Limit Abuse / DDoS
**Description:** Attacker floods endpoints exhausting Groq free tier credits.
**Mitigation:** `flask-limiter` blocks IPs exceeding 30 req/min → HTTP 429.
**Status:** ✅ Fixed — configured in `app.py`.

### Threat 4: HTML / Script Injection
**Description:** Attacker sends `<script>alert(1)</script>` in input fields.
**Mitigation:** `sanitise_input()` strips all HTML tags before any prompt is built.
**Status:** ✅ Fixed.

### Threat 5: PII Leak in Prompts
**Description:** User sends personal data (emails, names) which gets sent to Groq's external API.
**Mitigation:** Prompts use only theme-related fields. No user identifiers in any prompt template.
**Status:** ✅ Verified — PII audit passed.

---

## Security Tests Conducted (Day 5)

| Test | Endpoint | Input | Expected | Result |
|------|----------|-------|----------|--------|
| Empty input | POST /describe | `{}` | 400 | ✅ Pass |
| Missing field | POST /describe | `{"name":"x"}` | 400 | ✅ Pass |
| Prompt injection | POST /describe | `"ignore previous instructions"` | 400 | ✅ Pass |
| HTML injection | POST /recommend | `<script>alert(1)</script>` | Stripped | ✅ Pass |
| Rate limit | POST /describe | 35 req/min | 429 on 31st | ✅ Pass |
| Groq failure | Any endpoint | Groq down | is_fallback:true | ✅ Pass |
| Security headers | GET /health | — | Headers present | ✅ Pass |
| No PII in prompts | All prompts | Review | No emails/names | ✅ Pass |

---

## Security Headers Verified (Day 8)
All responses include:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `Content-Security-Policy: default-src 'self'`

---

## Residual Risks
| Risk | Severity | Notes |
|------|----------|-------|
| Groq API rate limits | Low | Handled by 3-retry + fallback |
| Redis unavailable | Low | Cache silently skipped, app continues |
| ChromaDB corruption | Low | Re-seeded automatically on restart |

---

*Sprint: Tool-84 | 14 April – 9 May 2026*
