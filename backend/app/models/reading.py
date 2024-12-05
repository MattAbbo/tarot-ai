# src/models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReadingRequest(BaseModel):
    context: str = ""
    reflection: str = ""

class UserThread(BaseModel):
    id: str
    device_id: str
    created_at: datetime
    last_active: datetime

class Reading(BaseModel):
    id: str
    question: Optional[str]
    card_drawn: str
    reflection: Optional[str]
    interpretation: str
    created_at: datetime
    thread_id: str
