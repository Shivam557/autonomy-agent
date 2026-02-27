# backend/llm/mock.py
import re
import asyncio
from .adapter import LLMAdapter

class MockAdapter:
    model_id = "mock-v1"

    async def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.2) -> str:
        # small artificial latency so logs/metrics behave like real LLM
        await asyncio.sleep(0.05)

        # Attempt to extract fields from the placeholder prompt lines:
        # Expecting lines like: "User: Alice", "Provider: Netflix", "Context: ...".
        user = re.search(r"User:\s*(.+)", prompt)
        prov = re.search(r"Provider:\s*(.+)", prompt)
        ctx  = re.search(r"Context:\s*([\s\S]+)", prompt)

        user_name = user.group(1).strip() if user else "Customer"
        provider = prov.group(1).strip() if prov else "Provider"
        context = ctx.group(1).strip() if ctx else "I would like to cancel."

        # Deterministic template — simple, editable
        subject = f"Request to cancel subscription with {provider}"
        body = (
            f"{subject}\n\n"
            f"Dear {provider} Support,\n\n"
            f"My name is {user_name}. {context}\n\n"
            f"I would like to request cancellation and a refund/waiver if applicable.\n\n"
            f"Thank you,\n{user_name}"
        )
        return body

    