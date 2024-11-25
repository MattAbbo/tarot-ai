# backend/app/routes/reading.py
import random
import uuid
from fastapi import APIRouter, HTTPException
from ..services.openai_service import OpenAIService
from ..services.image_service import ImageService
from ..services.langfuse_service import langfuse_service
from ..models.reading import ReadingRequest
from ..constants.cards import ALL_CARDS

router = APIRouter()

openai_service = OpenAIService()
image_service = ImageService()

@router.post("/reading")
async def get_reading(request: ReadingRequest):
    session_id = str(uuid.uuid4())
    
    try:
        # Initial card draw (no reflection provided)
        if not request.reflection:
            card = random.choice(ALL_CARDS)
            img_data = image_service.get_card_image(card)
            
            return {
                "card_name": card,
                "image_data": f"data:image/jpeg;base64,{img_data}",
                "session_id": session_id
            }
        
        # Get card name from the current reading
        card_name = request.card_name
        if not card_name or card_name not in ALL_CARDS:
            langfuse_service.track_error(
                session_id=session_id,
                error=f"Invalid card name: {card_name}",
                context="card_validation"
            )
            return {
                "interpretation": "I apologize, but I couldn't identify the card. Please try again.",
                "session_id": session_id
            }
        
        # Get interpretation from OpenAI
        interpretation_response = await openai_service.get_card_interpretation(
            card_name=card_name,
            context=request.context,  # This is just the question/thought
            reflection=request.reflection
        )
        
        # Extract interpretation and session_id
        interpretation = (
            interpretation_response["interpretation"] 
            if isinstance(interpretation_response, dict) 
            else interpretation_response
        )
        
        final_session_id = (
            interpretation_response.get("session_id") 
            if isinstance(interpretation_response, dict) 
            else session_id
        )

        return {
            "interpretation": interpretation,
            "session_id": final_session_id
        }

    except Exception as e:
        print(f"Error in get_reading: {str(e)}")
        langfuse_service.track_error(
            session_id=session_id,
            error=str(e),
            context="reading_route"
        )
        return {
            "interpretation": "I apologize, but I couldn't complete the reading. Please try again.",
            "session_id": session_id
        }

@router.post("/feedback")
async def submit_feedback(feedback_data: dict):
    try:
        langfuse_service.score_reading(
            session_id=feedback_data["session_id"],
            score=feedback_data["score"],
            feedback=feedback_data.get("feedback")
        )
        return {"status": "success"}
    except Exception as e:
        print(f"Error submitting feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to submit feedback")
