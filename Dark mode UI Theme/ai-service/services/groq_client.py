import os
import time
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

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
    response = requests.post(API_URL, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def call_groq_with_retry(prompt: str, retries=3) -> str:
    for attempt in range(retries):
        try:
            return call_groq(prompt)
        except Exception as e:
            logging.warning(f"Groq attempt {attempt+1} failed: {e}")
            time.sleep(2 ** attempt)
    raise Exception("All Groq retries failed")

# Test
if __name__ == "__main__":
    result = call_groq("Say hello in one sentence.")
    print(result)