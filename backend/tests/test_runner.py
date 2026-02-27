# backend/tests/test_runner.py
import asyncio
import os
import sys
from types import SimpleNamespace
from backend.llm.gemini import GeminiAdapter

# ensure project root is importable when running this script directly
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from backend.core.draft_service import generate_draft

# Dummy adapter for local tests only
class DummyAdapter:
    model_id = "dummy-v0"
    async def generate(self, prompt: str, max_tokens: int = 400, temperature: float = 0.2) -> str:
        # predictable canned output that matches validation rules
        return (
            "Dear Support Team,\n\n"
            "I am writing to cancel my subscription and request a refund. I request a refund of $49.99 for the recent renewal charged on 2026-02-10. "
            "I have been a customer for 14 months and the renewal was accidental. Please process the refund to the original payment method. "
            "Please confirm within 5 business days at anjali@example.com.\n\n"
            "Thank you,\nAnjali R"
        )

async def run():
    adapter = GeminiAdapter()
    # Create a minimal request object the draft_service expects.
    # We use SimpleNamespace so we don't have to import Pydantic models.
    req = SimpleNamespace(
        provider="AcmeCloud",
        user_name="Anjali R",
        context="Accidental auto-renewal; not using the service.",
        monthly_fee=49.99,   # optional, used for estimatedSavings
        months_left=0,       # optional
        # Include any other attributes your draft_service or templates might reference:
        service="Pro Dev Plan",
        account_id="AC-55421",
        tenure_months="14",
        last_payment_date="2026-02-10",
        contact_email="anjali@example.com"
    )

    result = await generate_draft(req, adapter)
    print("RESULT:", result)

if __name__ == "__main__":
    asyncio.run(run())