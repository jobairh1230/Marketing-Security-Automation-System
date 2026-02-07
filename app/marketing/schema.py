# Define JSON Schema for structured content (Marketing Content).
from pydantic import BaseModel, Field
from typing import List, Optional

class MarketingContent(BaseModel):
    content_type: str
    title: str
    subject: Optional[str] = None
    body: str
    cta: str
    disclaimers: List[str] = Field(default_factory=list)
    seo_keywords: List[str] = Field(default_factory=list)
    risk_flags: List[str] = Field(default_factory=list)
