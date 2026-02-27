# backend/llm/adapter.py
from typing import Protocol, Any

class LLMAdapter(Protocol):
    model_id: str

    async def generate(self, prompt: str, max_tokens: int = 400, temperature: float = 0.2) -> str:
        """Produce text for given prompt."""
        raise NotImplementedError("Implement in provider adapter (e.g., llm/gemini.py)")
    
    