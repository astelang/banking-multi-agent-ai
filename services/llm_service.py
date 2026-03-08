from openai import OpenAI
import os
from dotenv import load_dotenv
from cachetools import TTLCache, cached
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

cache = TTLCache(maxsize=1000, ttl=300)  # cache responses for 5 minutes

class LLMService:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    @cached(cache)
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def analyze(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content.strip()