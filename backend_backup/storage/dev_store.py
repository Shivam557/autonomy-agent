# backend/storage/dev_store.py
import json
from datetime import datetime
from typing import Dict, List, Optional
# from .dev_store import get_draft

FILE = "dev_drafts.jsonl"

def append_draft(draft: Dict) -> None:
    payload = {
        "draft_id": draft.get("draft_id"),
        "subject": draft.get("subject"),
        "body": draft.get("body"),
        "estimatedSavings": draft.get("estimatedSavings"),
        "meta": draft.get("meta"),
        "created_at": draft.get("created_at") or datetime.utcnow().isoformat() + "Z"
    }

    if get_draft(payload["draft_id"]) is not None:
        return 
    
    with open(FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _read_all_lines() -> List[Dict]:
    """Return list of parsed JSON objects (oldest -> newest). Ignore malformed lines."""
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        return []
    items: List[Dict] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            items.append(obj)
        except Exception:
            # skip bad line
            continue
    return items


def get_draft(draft_id: str) -> Optional[Dict]:
    """Return draft dict or None."""
    items = _read_all_lines()
    # file is oldest->newest; search from end for recent match
    for obj in reversed(items):
        if obj.get("draft_id") == draft_id:
            return obj
    return None


def list_drafts(limit: int = 20) -> List[Dict]:
    """Return most recent drafts up to limit, newest first."""
    items = _read_all_lines()
    if not items:
        return []
    # reverse to have newest first
    items = list(reversed(items))
    return items[:max(0, int(limit))]