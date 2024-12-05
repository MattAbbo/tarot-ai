import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from the backend/.env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Initialize services
from backend.app.services.supabase_service import SupabaseService
supabase_service = SupabaseService(supabase)

async def get_or_create_thread(device_id: str):
    """Get or create a thread for the given device_id"""
    return await supabase_service.get_or_create_thread(device_id)
