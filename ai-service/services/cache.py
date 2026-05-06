import redis
import os
import hashlib

_client = None

def get_redis():
    global _client
    if _client is None:
        try:
            _client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
            _client.ping()
        except Exception:
            _client = None
    return _client

TTL = 15 * 60  # 15 minutes — Day 7


def get_cached(prompt: str):
    r = get_redis()
    if not r:
        return None
    key = "ai:" + hashlib.sha256(prompt.encode()).hexdigest()
    try:
        val = r.get(key)
        return val.decode() if val else None
    except Exception:
        return None


def set_cached(prompt: str, response: str):
    r = get_redis()
    if not r:
        return
    key = "ai:" + hashlib.sha256(prompt.encode()).hexdigest()
    try:
        r.setex(key, TTL, response)
    except Exception:
        pass  # cache failure must never crash the app
