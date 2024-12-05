import os
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# Get the directory containing utils.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

# Load environment variables with explicit path
load_dotenv(ENV_PATH)

# Initialize Supabase
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

async def get_or_create_thread(device_id: str):
    """Get or create a thread for the given device_id"""
    try:
        # Try to find existing thread
        response = supabase.table('user_threads')\
            .select('*')\
            .eq('device_id', device_id)\
            .execute()
        
        if response.data:
            thread = response.data[0]
            # Update last_active
            supabase.table('user_threads')\
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
            response = supabase.table('user_threads')\
                .insert(thread_data)\
                .execute()
            thread = response.data[0]
        
        return thread
    except Exception as e:
        print(f"Thread error: {str(e)}")
        return None
