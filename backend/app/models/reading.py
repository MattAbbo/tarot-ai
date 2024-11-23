# src/models.py
from pydantic import BaseModel

class ReadingRequest(BaseModel):
    context: str = ""
    reflection: str = ""