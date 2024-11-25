# app/routes/reading.py
import random
import uuid
import logging
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from ..services.openai_service import OpenAIService
from ..services.image_service import ImageService
from ..services.langfuse_service import langfuse_service
from ..models.reading import ReadingRequest, FeedbackRequest
from ..constants.cards import ALL_CARDS

logger = logging.getLogger(__name__)

router = APIRouter()
openai_service = OpenAIService()
image_service = ImageService()

@router.post("/reading")
async def get_reading(request: ReadingRequest):
    session_id = request.session_id or str(uuid.uuid4())
    
    try:
        logger.debug("=== New Reading Request ===")
        logger.debug(f"Request data: {request}")
        
        # Initial card draw (no reflection provided)
        if not request.reflection:
            logger.debug("Initial card draw (no reflection)")
            card = random.choice(list(ALL_CARDS))
            img_data = image_service.get_card_image(card)
            
            return {
                "card_name": card,
                "image_data": f"data:image/jpeg;base64,{img_data}",
                "session_id": session_id
            }
        
        # Get interpretation for the card
        card_name = request.card_name
        logger.debug(f"Processing card interpretation request: {card_name}")
        
        if not card_name or card_name not in ALL_CARDS:
            error_msg = f"Invalid card name: {card_name}"
            logger.error(error_msg)
            await langfuse_service.track_error(
                session_id=session_id,
                error=error_msg,
                context="card_validation"
            )
            return {
                "error": "Invalid card",
                "message": "I apologize, but I couldn't identify the card. Please try again.",
                "session_id": session_id
            }
        
        logger.debug(f"Getting interpretation from OpenAI for card: {card_name}")
        logger.debug(f"Context: {request.context}")
        logger.debug(f"Reflection: {request.reflection}")
        
        # Get the streaming response generator
        interpretation_stream = openai_service.get_card_interpretation(
            card_name=card_name,
            context=request.context,
            reflection=request.reflection
        )
        
        # Return a streaming response
        return StreamingResponse(
            interpretation_stream,
            media_type="text/event-stream"
        )

    except Exception as e:
        error_msg = f"Error in get_reading: {str(e)}"
        logger.error(error_msg)
        logger.exception("Full traceback:")
        await langfuse_service.track_error(
            session_id=session_id,
            error=str(e),
            context="reading_route"
        )
        return {
            "error": "Internal error",
            "message": "I apologize, but I couldn't complete the reading. Please try again.",
            "session_id": session_id
        }
