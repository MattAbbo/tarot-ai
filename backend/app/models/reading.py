# src/models/reading.py
from pydantic import BaseModel
from typing import Optional

class ReadingRequest(BaseModel):
    context: Optional[str] = None     # User's question or thought
    reflection: Optional[str] = None   # User's reflection on the card
    card_name: Optional[str] = None   # The drawn card's name
    session_id: Optional[str] = None  # Track session across reading flow

class FeedbackRequest(BaseModel):
    session_id: str
    score: float  # 0-1 score for the reading quality
    feedback: Optional[str] = None  # Optional user feedback text
