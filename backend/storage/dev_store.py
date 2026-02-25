# backend/storage/dev_store.py
import json
from datetime import datetime
from typing import Dict

FILE = "dev_drafts.jsonl"

def append_draft(draft: Dict) -> None:
    payload = {
        "draft_id": draft.get("draft_id"),
        "subject": draft.get("subject"),
        "body": draft.get("body"),
        "estimatedSavings": draft.get("estimatedSavings"),
        "meta": draft.get("meta"),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    with open(FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")