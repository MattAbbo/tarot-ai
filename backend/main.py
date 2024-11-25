import os
import logging
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Resolve directories
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
ENV_PATH = BASE_DIR / ".env"

# Load environment variables
logger.info(f"Resolved ENV_PATH: {ENV_PATH}")
if not ENV_PATH.exists() or not os.access(ENV_PATH, os.R_OK):
    logger.critical(f"Critical Error: Cannot load .env file at {ENV_PATH}")
    raise RuntimeError("Failed to load .env file. Check path and permissions.")
load_dotenv(ENV_PATH)
logger.info(f"Loading .env from: {ENV_PATH}")

# Verify environment variables
openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    logger.info(f"OPENAI_API_KEY loaded successfully: {openai_key[:6]}...")
else:
    logger.error("OPENAI_API_KEY not loaded. Check .env file or system variables.")

# FastAPI app instance
app = FastAPI()

# Middleware: Debugging
@app.middleware("http")
async def debug_middleware(request: Request, call_next):
    logger.debug(f"Method: {request.method}, URL: {request.url}")
    try:
        if "application/json" in request.headers.get("content-type", ""):
            body = await request.body()
            logger.debug(f"Request Body: {body.decode()[:500]}...")
    except Exception as e:
        logger.error(f"Error reading request body: {e}")

    response = await call_next(request)
    logger.debug(f"Response Status: {response.status_code}")
    return response

# Middleware: CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware: Global error handler
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
                "method": request.method,
            },
        )

# Static files
STATIC_DIR = BASE_DIR / "static"
SRC_DIR = ROOT_DIR / "src"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/src", StaticFiles(directory=SRC_DIR), name="src")

# Add routers
from app.routes.reading import router as reading_router
from app.routes.image import router as image_router

app.include_router(reading_router, prefix="/api")
app.include_router(image_router, prefix="/api")

@app.get("/")
async def read_root():
    return FileResponse(ROOT_DIR / "index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="debug",
        access_log=True,
    )