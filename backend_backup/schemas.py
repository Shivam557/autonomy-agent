from typing import Optional, Dict
from pydantic import BaseModel, Field, constr, conint, confloat

class GenerateRequest(BaseModel):
    user_name: constr(min_length=1, max_length=100)
    provider: constr(min_length=1, max_length=100)
    context: constr(min_length=1, max_length=2000)
    monthly_fee: Optional[confloat(ge=0, le=100000)] = None
    months_left: Optional[conint(ge=0, le=120)] = None
    request_id: Optional[constr(pattern=r'^[A-Za-z0-9\-_]{1,64}$')] = None

class GenerateResponse(BaseModel):
    subject: str
    bodyPreview: str
    estimatedSavings: Optional[float] = None
    meta: dict = Field(default_factory=dict)


class DraftListItem(BaseModel):
    draft_id: str
    subject: str
    bodyPreview: str
    estimatedSavings: Optional[float] = None
    meta: Dict = {}
    created_at: Optional[str] = None
    
class DraftResponse(BaseModel):
    draft_id: str
    subject: str
    body: str
    estimatedSavings: Optional[float] = None
    meta: Dict = {}
    created_at: Optional[str] = None

