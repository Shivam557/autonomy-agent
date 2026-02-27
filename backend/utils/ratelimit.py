# backend/utils/ratelimit.py
import time
import threading
from collections import deque
from typing import Deque, Dict

_LOCK = threading.Lock()
_STORE: Dict[str, Deque[float]] = {}

def is_allowed(key: str, limit: int = 10, window_seconds: int = 60) -> bool:
    """
    Simple sliding-window rate limiter.
    - key: usually client IP or API key
    - limit: max requests in window
    - window_seconds: time window in seconds
    Returns True if request is allowed.
    """
    now = time.time()
    cutoff = now - window_seconds
    with _LOCK:
        q = _STORE.get(key)
        if q is None:
            q = deque()
            _STORE[key] = q
        # pop old
        while q and q[0] < cutoff:
            q.popleft()
        if len(q) >= limit:
            return False
        q.append(now)
        return True