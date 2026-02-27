# backend/main.py
import time
import logging
from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.schemas import GenerateRequest, GenerateResponse, DraftResponse, DraftListItem
from backend.llm.gemini import GeminiAdapter  # or fallback to MockAdapter in tests
from backend.core.draft_service import generate_draft
from backend.storage.dev_store import append_draft, get_draft, list_drafts
from backend.utils.ratelimit import is_allowed

# --- logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
logger = logging.getLogger("backend")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adapter: real or fallback
try:
    adapter = GeminiAdapter()
except Exception as e:
    logger.warning("GeminiAdapter init failed, falling back to mock: %s", e)
    from backend.llm.mock import MockAdapter
    adapter = MockAdapter()

# ------- Error handlers (consistent JSON) -------
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail, "code": exc.status_code})

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error: %s", exc)
    return JSONResponse(status_code=500, content={"error": "internal_error", "code": 500, "details": str(exc)})

# health
@app.get("/")
async def health_check():
    return {"status": "backend running"}

# POST generate with idempotency and rate limiting
@app.post("/api/v1/generate-draft", response_model=GenerateResponse)
async def api_generate(req: GenerateRequest, background_tasks: BackgroundTasks, request: Request = None):
    # rate limit
    client_ip = (request.client.host if request and request.client else "unknown")
    if not is_allowed(client_ip, limit=3, window_seconds=60):
        raise HTTPException(status_code=429, detail="rate_limit_exceeded")

    # idempotency: if client provided request_id and a draft with that id exists, return it
    if req.request_id:
        existing = get_draft(req.request_id)
        if existing:
            logger.info("Idempotent hit for request_id=%s from %s", req.request_id, client_ip)
            return {
                "subject": existing.get("subject"),
                "bodyPreview": (existing.get("body") or "")[:400],
                "estimatedSavings": existing.get("estimatedSavings"),
                "meta": existing.get("meta", {})
            }

    start = time.time()
    try:
        result = await generate_draft(req, adapter)
    except Exception as e:
        logger.error("LLM generation failed: %s", e)
        raise HTTPException(status_code=503, detail="llm_unavailable")

    latency_ms = int((time.time() - start) * 1000)
    draft_id = req.request_id or f"dev-{int(time.time()*1000)}"

    stored = {
        "draft_id": draft_id,
        "subject": result["subject"],
        "body": result["body"],
        "estimatedSavings": result["estimatedSavings"],
        "meta": {**result["meta"], "latency_ms": latency_ms},
        "created_at": None
    }

    # persist in background
    # background_tasks.add_task(append_draft, stored)
    append_draft(stored)

    logger.info("Generated draft_id=%s provider=%s client=%s model=%s latency=%dms",
                draft_id, req.provider, client_ip, stored["meta"].get("model_id"), latency_ms)

    return {
        "subject": result["subject"],
        "bodyPreview": result["bodyPreview"],
        "estimatedSavings": result["estimatedSavings"],
        "meta": stored["meta"]
    }

# GET single draft
@app.get("/api/v1/draft/{draft_id}", response_model=DraftResponse)
async def api_get_draft(draft_id: str):
    draft = get_draft(draft_id)
    if not draft:
        raise HTTPException(status_code=404, detail="not_found")
    return {
        "draft_id": draft.get("draft_id"),
        "subject": draft.get("subject"),
        "body": draft.get("body"),
        "estimatedSavings": draft.get("estimatedSavings"),
        "meta": draft.get("meta", {}),
        "created_at": draft.get("created_at"),
    }

# GET list of drafts
@app.get("/api/v1/drafts", response_model=list[DraftListItem])
async def api_list_drafts(limit: int = 20):
    items = list_drafts(limit=limit)
    out = []
    for obj in items:
        out.append({
            "draft_id": obj.get("draft_id"),
            "subject": obj.get("subject"),
            "bodyPreview": (obj.get("body") or "")[:400],
            "estimatedSavings": obj.get("estimatedSavings"),
            "created_at": obj.get("created_at"),
            "meta": obj.get("meta", {}),
        })
    return out
