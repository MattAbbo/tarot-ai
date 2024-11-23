import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

# Get the directory containing main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))  # Root of the project
ENV_PATH = os.path.join(BASE_DIR, ".env")

# Load environment variables with explicit path
load_dotenv(ENV_PATH)
print(f"Loading .env from: {ENV_PATH}")

# Update imports to use relative imports
from .app.routes.reading import router as reading_router
from .app.routes.audio import router as audio_router
from .app.routes.image import router as image_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files in the backend/static directory
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Mount the src directory containing React components
app.mount("/src", StaticFiles(directory=os.path.join(ROOT_DIR, "src")), name="src")

# Mount routers with prefixes
app.include_router(reading_router, prefix="/api")
app.include_router(audio_router, prefix="/api")
app.include_router(image_router, prefix="/api")

@app.get("/")
async def read_root():
    # Serve the index.html file from the root directory
    return FileResponse(os.path.join(ROOT_DIR, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
