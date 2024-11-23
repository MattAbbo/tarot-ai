# src/routes/reading.py
import random
from fastapi import APIRouter
from ..services.openai_service import OpenAIService
from ..services.image_service import ImageService
from ..models.reading import ReadingRequest
from ..constants.cards import ALL_CARDS

router = APIRouter()

openai_service = OpenAIService()
image_service = ImageService()

@router.post("/reading")
async def get_reading(request: ReadingRequest):
    try:
        if not request.reflection:
            card = random.choice(ALL_CARDS)
            img_data = image_service.get_card_image(card)
            
            return {
                "card_name": card,
                "image_data": f"data:image/jpeg;base64,{img_data}"
            }
        
        if "CARD:" not in request.context:
            return {
                "interpretation": "I apologize, but I couldn't identify which card was drawn. Please try again."
            }
        
        card_name = request.context.split("CARD:")[1].strip()
        if not card_name or card_name not in ALL_CARDS:
            return {
                "interpretation": "I apologize, but I couldn't identify the card. Please try again."
            }
        
        interpretation = await openai_service.get_card_interpretation(
            card_name=card_name,
            context=request.context,
            reflection=request.reflection
        )

        return {"interpretation": interpretation}

    except Exception as e:
        print(f"Error in get_reading: {str(e)}")  # Add logging for debugging
        return {
            "interpretation": "I apologize, but I couldn't complete the reading. Please try again."
        }
