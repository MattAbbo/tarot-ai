from datetime import datetime
import random
import os
import logging
from typing import Dict, Any

from backend.app.constants.cards import ALL_CARDS, MAJOR_ARCANA_MAP, MINOR_ARCANA_MAP
from backend.app.models.reading import ReadingRecord, ThreadStats
from backend.app.services.openai_service import OpenAIService
from backend.app.services.supabase_service import SupabaseService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReadingService:
    def __init__(self, supabase_service: SupabaseService, openai_service: OpenAIService):
        self.supabase = supabase_service
        self.openai_service = openai_service

    async def draw_card(self, thread_id: str, question: str) -> Dict[str, str]:
        """Draw a card and store the initial reading data"""
        card = random.choice(ALL_CARDS)
        
        reading_data = ReadingRecord(
            thread_id=thread_id,
            question=question,
            card_drawn=card,
            created_at=datetime.utcnow()  # Keep as datetime object
        )
        
        await self.supabase.create_reading(reading_data)
        
        # Get the correct image filename from either major or minor arcana maps
        if card in MAJOR_ARCANA_MAP:
            image_filename = MAJOR_ARCANA_MAP[card]
        else:
            image_filename = MINOR_ARCANA_MAP[card]
        
        # Construct the image path
        image_path = f"/static/cards/{image_filename}"
        
        # Log the card draw details
        logger.info(f"Drew card: {card}")
        logger.info(f"Image filename: {image_filename}")
        logger.info(f"Image path: {image_path}")
        
        # Verify the image file exists
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        full_path = os.path.join(base_dir, "static", "cards", image_filename)
        if not os.path.exists(full_path):
            logger.error(f"Card image not found: {full_path}")
        else:
            logger.info(f"Card image exists at: {full_path}")
        
        return {
            "card_name": card,
            "image_path": image_path
        }

    async def get_interpretation(self, thread_id: str, card_drawn: str, question: str, reflection: str) -> str:
        """Get card interpretation and update the reading record"""
        interpretation = await self.openai_service.get_card_interpretation(
            card_name=card_drawn,
            context=question,
            reflection=reflection
        )
        
        await self.supabase.update_reading(
            thread_id=thread_id,
            card_drawn=card_drawn,
            reflection=reflection,
            interpretation=interpretation
        )
        
        return interpretation

    async def get_thread_statistics(self, thread_id: str, thread_created_at: datetime) -> ThreadStats:
        """Get statistics for a reading thread"""
        stats = await self.supabase.get_thread_stats(thread_id)
        
        if not stats:
            return ThreadStats(
                total_readings=0,
                last_reading_date=None,
                thread_created=thread_created_at
            )
            
        return ThreadStats(
            total_readings=stats['count'],
            last_reading_date=stats['max'],
            thread_created=thread_created_at
        )
