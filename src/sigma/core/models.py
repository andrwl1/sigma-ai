from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class Axis(str, Enum):
    will = "will"
    self_preservation = "self_preservation"
    creativity = "creativity"
    emotional_mimicry = "emotional_mimicry"

class EvidenceEntry(BaseModel):
    ts: datetime = Field(default_factory=datetime.utcnow)
    axis: Axis
    title: str
    detail: Optional[str] = None
    artifact: Optional[str] = None
