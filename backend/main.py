import os
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uuid

from backend.app.services.reading_service import ReadingService
from backend.app.services.openai_service import OpenAIService
from backend.utils import supabase_service
from backend.app.routes.reading import router as reading_router
from backend.app.routes.image import router as image_router

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services
openai_service = OpenAIService()
reading_service = ReadingService(supabase_service, openai_service)

# Get absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
STATIC_DIR = os.path.join(BASE_DIR, "static")
CARDS_DIR = os.path.join(STATIC_DIR, "cards")

# Verify directories exist
if not os.path.exists(STATIC_DIR):
    raise RuntimeError(f"Static directory not found: {STATIC_DIR}")
if not os.path.exists(CARDS_DIR):
    raise RuntimeError(f"Cards directory not found: {CARDS_DIR}")

# Log directory paths for debugging
logger.info(f"BASE_DIR: {BASE_DIR}")
logger.info(f"ROOT_DIR: {ROOT_DIR}")
logger.info(f"STATIC_DIR: {STATIC_DIR}")
logger.info(f"CARDS_DIR: {CARDS_DIR}")

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.middleware("http")
async def add_device_id(request: Request, call_next):
    device_id = request.headers.get("X-Device-ID")
    if not device_id:
        device_id = str(uuid.uuid4())
    request.state.device_id = device_id
    
    # Log request details
    logger.info(f"Request path: {request.url.path}")
    if request.url.path.startswith('/static/'):
        logger.info(f"Static file request: {request.url.path}")
        file_path = os.path.join(STATIC_DIR, *request.url.path.split('/')[2:])
        logger.info(f"Absolute file path: {file_path}")
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
    
    response = await call_next(request)
    
    if not request.headers.get("X-Device-ID"):
        response.headers["X-Device-ID"] = device_id
    
    return response

# Custom static files handler
class CustomStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        logger.info(f"Attempting to serve static file: {path}")
        try:
            response = await super().get_response(path, scope)
            logger.info(f"Static file response status: {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"Error serving static file {path}: {str(e)}")
            raise HTTPException(status_code=404, detail=f"File not found: {path}")

# Mount static files
static_files = CustomStaticFiles(
    directory=STATIC_DIR,
    html=True,
    check_dir=True
)
app.mount("/static", static_files, name="static")

# Mount React components
app.mount("/src", StaticFiles(directory=os.path.join(ROOT_DIR, "src")), name="src")

# Mount API routers
app.include_router(reading_router, prefix="/api")
app.include_router(image_router, prefix="/api")

@app.get("/static/cards/{filename}")
async def get_card_image(filename: str):
    """Explicit handler for card images"""
    file_path = os.path.join(CARDS_DIR, filename)
    logger.info(f"Requested card image: {file_path}")
    if not os.path.exists(file_path):
        logger.error(f"Card image not found: {file_path}")
        raise HTTPException(status_code=404, detail="Card image not found")
    return FileResponse(file_path)

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(ROOT_DIR, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
