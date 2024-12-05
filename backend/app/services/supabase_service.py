import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from supabase import Client

from backend.app.models.reading import ReadingRecord, ThreadStats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseService:
    def __init__(self, client: Client):
        self.client = client

    async def get_or_create_thread(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Get or create a thread for the given device_id"""
        try:
            # Try to find existing thread
            response = self.client.table('user_threads')\
                .select('*')\
                .eq('device_id', device_id)\
                .execute()
            
            if response.data:
                thread = response.data[0]
                # Update last_active
                self.client.table('user_threads')\
                    .update({'last_active': datetime.utcnow().isoformat()})\
                    .eq('id', thread['id'])\
                    .execute()
            else:
                # Create new thread
                thread_data = {
                    'device_id': device_id,
                    'created_at': datetime.utcnow().isoformat(),
                    'last_active': datetime.utcnow().isoformat()
                }
                response = self.client.table('user_threads')\
                    .insert(thread_data)\
                    .execute()
                thread = response.data[0]
            
            return thread
        except Exception as e:
            logger.error(f"Error in get_or_create_thread: {str(e)}")
            return None

    async def create_reading(self, reading: ReadingRecord) -> Optional[Dict[str, Any]]:
        """Create a new reading record"""
        try:
            # Convert to dict and ensure datetime is serialized to ISO format
            reading_dict = reading.dict()
            reading_dict['created_at'] = reading.created_at.isoformat()
            
            response = self.client.table('readings')\
                .insert(reading_dict)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error in create_reading: {str(e)}")
            return None

    async def update_reading(self, thread_id: str, card_drawn: str, 
                           reflection: str, interpretation: str) -> bool:
        """Update a reading with reflection and interpretation"""
        try:
            response = self.client.table('readings')\
                .update({
                    "reflection": reflection,
                    "interpretation": interpretation
                })\
                .eq('thread_id', thread_id)\
                .eq('card_drawn', card_drawn)\
                .is_('interpretation', 'null')\
                .execute()
            return bool(response.data)
        except Exception as e:
            logger.error(f"Error in update_reading: {str(e)}")
            return False

    async def get_thread_stats(self, thread_id: str) -> Optional[Dict[str, Any]]:
        """Get statistics for a reading thread"""
        try:
            response = self.client.table('readings')\
                .select('count(*), max(created_at)')\
                .eq('thread_id', thread_id)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error in get_thread_stats: {str(e)}")
            return None

    async def get_thread_readings(self, thread_id: str) -> List[Dict[str, Any]]:
        """Get all readings for a thread"""
        try:
            response = self.client.table('readings')\
                .select('*')\
                .eq('thread_id', thread_id)\
                .order('created_at', desc=True)\
                .execute()
            return response.data
        except Exception as e:
            logger.error(f"Error in get_thread_readings: {str(e)}")
            return []

    async def delete_thread(self, thread_id: str) -> bool:
        """Delete a thread and all its readings"""
        try:
            # Delete readings first (foreign key constraint)
            self.client.table('readings')\
                .delete()\
                .eq('thread_id', thread_id)\
                .execute()
            
            # Then delete the thread
            response = self.client.table('user_threads')\
                .delete()\
                .eq('id', thread_id)\
                .execute()
            return bool(response.data)
        except Exception as e:
            logger.error(f"Error in delete_thread: {str(e)}")
            return False

    async def cleanup_inactive_threads(self, days: int = 30) -> int:
        """Delete threads that have been inactive for more than specified days"""
        try:
            cutoff_date = (datetime.utcnow() - datetime.timedelta(days=days)).isoformat()
            response = self.client.table('user_threads')\
                .delete()\
                .lt('last_active', cutoff_date)\
                .execute()
            return len(response.data)
        except Exception as e:
            logger.error(f"Error in cleanup_inactive_threads: {str(e)}")
            return 0
