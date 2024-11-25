# main.py
import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get the directory containing main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))  # Root of the project
ENV_PATH = os.path.join(BASE_DIR, ".env")

# Load environment variables with explicit path
load_dotenv(ENV_PATH)
logger.info(f"Loading .env from: {ENV_PATH}")

# Use absolute imports
from app.routes.reading import router as reading_router
from app.routes.image import router as image_router

app = FastAPI()

# Add debug middleware
@app.middleware("http")
async def debug_middleware(request: Request, call_next):
    # Log request details
    logger.debug("=== Incoming Request ===")
    logger.debug(f"Method: {request.method}")
    logger.debug(f"URL: {request.url}")
    logger.debug(f"Headers: {dict(request.headers)}")
    
    # Try to read and log the body
    try:
        body = await request.body()
        if body:
            body_str = body.decode()
            logger.debug(f"Request Body: {body_str}")
            # Store body for route handlers
            setattr(request.state, 'body', body_str)
    except Exception as e:
        logger.error(f"Error reading request body: {e}")

    # Process the request
    response = await call_next(request)
    
    # Log response details
    logger.debug("=== Response ===")
    logger.debug(f"Status: {response.status_code}")
    
    return response

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global error handler
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.error(f"Global error handler caught: {str(e)}")
        logger.exception("Full traceback:")
        return JSONResponse(
            status_code=500,
            content={
                "detail": str(e),
                "path": request.url.path,
                "method": request.method
            }
        )

# Mount static files in the backend/static directory
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Mount the src directory containing React components
app.mount("/src", StaticFiles(directory=os.path.join(ROOT_DIR, "src")), name="src")

# Mount routers with prefixes
app.include_router(reading_router, prefix="/api")
app.include_router(image_router, prefix="/api")

@app.get("/")
async def read_root():
    # Serve the index.html file from the root directory
    return FileResponse(os.path.join(ROOT_DIR, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="debug"
    )