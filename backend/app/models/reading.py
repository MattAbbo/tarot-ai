from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Request Models
class DrawRequest(BaseModel):
    question: str

class InterpretationRequest(BaseModel):
    card_drawn: str
    question: str
    reflection: str

# Response Models
class DrawResponse(BaseModel):
    card_name: str
    image_path: str

class InterpretationResponse(BaseModel):
    interpretation: str

class ThreadStats(BaseModel):
    total_readings: int
    last_reading_date: Optional[datetime]
    thread_created: datetime

# Database Models
class ReadingRecord(BaseModel):
    thread_id: str
    question: str
    card_drawn: str
    reflection: Optional[str] = None
    interpretation: Optional[str] = None
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
