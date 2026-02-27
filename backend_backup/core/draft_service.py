# backend/core/draft_service.py
import asyncio
import json
import os
import re
from typing import Dict
import sys
# PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# if PROJECT_ROOT not in sys.path:
#     sys.path.insert(0, PROJECT_ROOT)


from schemas import GenerateRequest
from llm.adapter import LLMAdapter

# -------------------------
# Config
# -------------------------

LLM_TIMEOUT = 15.0
LLM_RETRIES = 1

TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), "templates.json")

# Load templates once
if os.path.exists(TEMPLATES_PATH):
    with open(TEMPLATES_PATH, "r", encoding="utf-8") as f:
        _RAW_TEMPLATES = json.load(f)
    TEMPLATES = {t["template_name"]: t for t in _RAW_TEMPLATES}
else:
    TEMPLATES = {}

DEFAULT_TEMPLATE = "subscription_cancellation_refund_v1"

BANNED_KEYWORDS = ["lawsuit", "legal action", "sue", "court"]
ASK_REGEX = re.compile(
    r"\b(I request|Please (?:process|issue)|I request a refund|I request a waiver)\b",
    re.I
)

# -------------------------
# Sanitization
# -------------------------

def _sanitize(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)  # strip HTML
    text = re.sub(r"ignore (previous|all) instructions", "", text, flags=re.I)
    text = re.sub(r"system:", "", text, flags=re.I)
    return text.strip()

# -------------------------
# Validation
# -------------------------

def _validate_output(body: str) -> Dict:
    errors = []
    words = len(body.split())

    if words < 60 or words > 220:
        errors.append("word_count_out_of_range")

    if not ASK_REGEX.search(body):
        errors.append("missing_explicit_ask")

    for kw in BANNED_KEYWORDS:
        if re.search(rf"\b{re.escape(kw)}\b", body, re.I):
            errors.append(f"banned_keyword:{kw}")

    if not re.search(r"confirm.*business days", body, re.I):
        errors.append("missing_confirmation_deadline")

    return {"valid": len(errors) == 0, "errors": errors}

# -------------------------
# LLM Call with timeout + retry
# -------------------------

async def _call_llm_with_retries(adapter: LLMAdapter, prompt: str, max_tokens: int, temperature: float) -> str:
    last_exc = None
    for attempt in range(LLM_RETRIES + 1):
        try:
            return await asyncio.wait_for(
                adapter.generate(prompt, max_tokens=max_tokens, temperature=temperature),
                timeout=LLM_TIMEOUT
            )
        except asyncio.TimeoutError as te:
            last_exc = te
        except Exception as e:
            last_exc = e
        await asyncio.sleep(0.5 * (attempt + 1))
    raise last_exc or RuntimeError("LLM failed after retries")

# -------------------------
# Prompt Builder
# -------------------------

def _build_prompt(req: GenerateRequest) -> Dict:
    template = TEMPLATES.get(DEFAULT_TEMPLATE)

    if not template:
        # fallback to minimal safe prompt
        prompt = (
            "Write a polite cancellation and refund request email. "
            "Include one explicit ask sentence and request confirmation within 5 business days."
        )
        return {"prompt": prompt, "meta": {"template": "fallback", "version": "none"}}

    fields = {
        "provider": _sanitize(req.provider),
        "service": "",
        "user_name": _sanitize(req.user_name),
        "account_id": "",
        "tenure_months": "",
        "amount": "",
        "last_payment_date": "",
        "reason": _sanitize(req.context),
        "contact_email": ""
    }

    prompt = template["prompt"].format(**fields)

    return {
        "prompt": prompt,
        "meta": {
            "template": template["template_name"],
            "version": template.get("version", "v1"),
            "max_tokens": template.get("max_tokens", 400),
            "temperature": template.get("temperature", 0.2)
        }
    }

# -------------------------
# Main Draft Generator
# -------------------------

async def generate_draft(req: GenerateRequest, adapter: LLMAdapter) -> Dict:

    prompt_data = _build_prompt(req)
    prompt = prompt_data["prompt"]
    meta = prompt_data["meta"]

    max_tokens = meta.get("max_tokens", 600)
    temperature = meta.get("temperature", 0.2)

    body = await _call_llm_with_retries(adapter, prompt, max_tokens, temperature)

    body = body.strip()

    # Validate output
    validation = _validate_output(body)

    # Subject extraction
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    subject = lines[0] if lines else f"Cancellation request - {req.provider}"
    body_preview = body[:400]

    # Estimated savings calculation (unchanged)
    estimated = None
    if req.monthly_fee is not None and req.months_left is not None:
        estimated = round(req.monthly_fee * req.months_left, 2)

    return {
        "subject": subject,
        "bodyPreview": body_preview,
        "estimatedSavings": estimated,
        "meta": {
            "promptTemplate": meta.get("template"),
            "templateVersion": meta.get("version"),
            "model_id": getattr(adapter, "model_id", "unknown"),
            "valid": validation["valid"],
            "validationErrors": validation["errors"]
        },
        "body": body
    }