import redis
import os
import hashlib

r = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
TTL = 15 * 60  # 15 minutes


def get_cached(prompt: str):
    key = "ai:" + hashlib.sha256(prompt.encode()).hexdigest()
    try:
        val = r.get(key)
        return val.decode() if val else None
    except Exception:
        return None


def set_cached(prompt: str, response: str):
    key = "ai:" + hashlib.sha256(prompt.encode()).hexdigest()
    try:
        r.setex(key, TTL, response)
    except Exception:
        pass  # cache failure must never crash the app
