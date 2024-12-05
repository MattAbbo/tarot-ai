from fastapi import APIRouter, Request, HTTPException

from backend.app.models.reading import (
    DrawRequest, 
    InterpretationRequest,
    DrawResponse,
    InterpretationResponse,
    ThreadStats
)
from backend.app.services.reading_service import ReadingService
from backend.app.services.openai_service import OpenAIService
from backend.utils import get_or_create_thread, supabase_service

router = APIRouter()
openai_service = OpenAIService()
reading_service = ReadingService(supabase_service=supabase_service, openai_service=openai_service)

@router.post("/reading", response_model=DrawResponse)
async def handle_reading(request: Request):
    """Handle both drawing a card and getting interpretation"""
    data = await request.json()
    device_id = request.state.device_id
    thread = await get_or_create_thread(device_id)
    
    if not thread:
        raise HTTPException(status_code=500, detail="Failed to create or get thread")
    
    # If reflection is provided, it's an interpretation request
    if "reflection" in data:
        interpretation = await reading_service.get_interpretation(
            thread_id=thread["id"],
            card_drawn=data["context"].split("CARD: ")[1],
            question=data["context"].split("CARD: ")[0].strip(),
            reflection=data["reflection"]
        )
        return {"interpretation": interpretation}
    
    # Otherwise, it's a draw request
    result = await reading_service.draw_card(
        thread_id=thread["id"],
        question=data.get("context", "")
    )
    
    return result

@router.get("/thread", response_model=ThreadStats)
async def get_thread_stats(req: Request):
    """Get statistics for the current reading thread"""
    device_id = req.state.device_id
    thread = await get_or_create_thread(device_id)
    
    if not thread:
        raise HTTPException(status_code=500, detail="Failed to create or get thread")
    
    return await reading_service.get_thread_statistics(
        thread_id=thread["id"],
        thread_created_at=thread["created_at"]
    )
