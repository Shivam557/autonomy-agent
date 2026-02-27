import os
import asyncio
from google import genai
from backend.llm.adapter import LLMAdapter


class GeminiAdapter(LLMAdapter):
    model_id = "gemini-2.5-flash"

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set")
        self.client = genai.Client(api_key=api_key)

    async def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.2) -> str:
        loop = asyncio.get_running_loop()

        def _call():
            resp = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config={
                    "max_output_tokens": max_tokens,
                    "temperature": temperature,
                }
            )
            return resp.text
               

        return await loop.run_in_executor(None, _call)
