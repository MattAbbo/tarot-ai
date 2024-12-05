# src/routes/reading.py
import random
from fastapi import APIRouter, Request
from ..services.openai_service import OpenAIService
from ..services.image_service import ImageService
from ..models.reading import ReadingRequest, Reading, UserThread
from ..constants.cards import ALL_CARDS
from ..utils import supabase, get_or_create_thread
from datetime import datetime

router = APIRouter()

openai_service = OpenAIService()
image_service = ImageService()

@router.post("/reading")
async def get_reading(request: ReadingRequest, req: Request):
    try:
        device_id = req.state.device_id
        thread = await get_or_create_thread(device_id)
        if not thread:
            return {"error": "Could not create thread"}

        if not request.reflection:
            # Initial request - draw a card
            card = random.choice(ALL_CARDS)
            img_data = image_service.get_card_image(card)
            
            # Store the card draw in the database
            reading_data = {
                "thread_id": thread["id"],
                "question": request.context,  # The initial question/context
                "card_drawn": card,
                "created_at": datetime.utcnow().isoformat()
            }
            supabase.table('readings').insert(reading_data).execute()
            
            return {
                "card_name": card,
                "image_data": f"data:image/jpeg;base64,{img_data}"
            }
        
        # Get card from context
        if "CARD:" not in request.context:
            return {
                "error": "Could not identify the card drawn"
            }
        
        card_name = request.context.split("CARD:")[1].strip()
        if not card_name or card_name not in ALL_CARDS:
            return {
                "error": "Invalid card name"
            }
        
        # Get interpretation from OpenAI
        interpretation = await openai_service.get_card_interpretation(
            card_name=card_name,
            context=request.context,
            reflection=request.reflection
        )

        # Update the reading with reflection and interpretation
        supabase.table('readings')\
            .update({
                "reflection": request.reflection,
                "interpretation": interpretation
            })\
            .eq('thread_id', thread["id"])\
            .eq('card_drawn', card_name)\
            .is_('interpretation', 'null')\
            .execute()

        return {"interpretation": interpretation}

    except Exception as e:
        print(f"Error in get_reading: {str(e)}")
        return {
            "error": "Could not complete the reading"
        }

@router.get("/readings")
async def get_readings(req: Request):
    """Get all readings for the device's thread"""
    try:
        device_id = req.state.device_id
        thread = await get_or_create_thread(device_id)
        if not thread:
            return {"readings": []}
        
        # Get readings for this thread
        response = supabase.table('readings')\
            .select('*')\
            .eq('thread_id', thread['id'])\
            .order('created_at', desc=True)\
            .execute()
        
        return {"readings": response.data}
    except Exception as e:
        print(f"Error getting readings: {str(e)}")
        return {"readings": []}

@router.get("/thread")
async def get_thread(req: Request):
    """Get current thread info"""
    try:
        device_id = req.state.device_id
        thread = await get_or_create_thread(device_id)
        if thread:
            return UserThread(**thread)
        return {"error": "Could not get thread"}
    except Exception as e:
        print(f"Error getting thread: {str(e)}")
        return {"error": "Could not get thread"}
