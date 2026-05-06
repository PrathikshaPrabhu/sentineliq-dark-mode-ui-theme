import os
import re
import time
import logging
import requests
from dotenv import load_dotenv
from services.cache import get_cached, set_cached

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

logging.basicConfig(level=logging.INFO)


# Day 3 — Input sanitisation + prompt injection detection
def sanitise_input(text: str) -> str:
    # Strip HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Detect prompt injection patterns
    injection_patterns = [
        r'ignore previous instructions',
        r'ignore all instructions',
        r'forget everything',
        r'act as',
        r'you are now',
        r'disregard',
        r'system prompt',
        r'jailbreak',
    ]
    for pattern in injection_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            raise ValueError("Potential prompt injection detected")
    return text.strip()


def call_groq(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 1000
    }
    response = requests.post(API_URL, headers=headers, json=body, timeout=10)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


# Day 2 — 3-retry with exponential backoff
# Day 7 — Redis cache check before calling Groq
def call_groq_with_retry(prompt: str, retries=3) -> str:
    cached = get_cached(prompt)
    if cached:
        logging.info("Cache hit — skipping Groq call")
        return cached

    for attempt in range(retries):
        try:
            result = call_groq(prompt)
            set_cached(prompt, result)
            return result
        except Exception as e:
            logging.warning(f"Groq attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)

    raise Exception("All Groq retries failed")


if __name__ == "__main__":
    result = call_groq_with_retry("Say hello in one sentence.")
    print(result)
