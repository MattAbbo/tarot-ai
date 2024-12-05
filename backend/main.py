import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uuid

# Get the directory containing main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))  # Root of the project

# Use absolute imports
from app.routes.reading import router as reading_router
from app.routes.image import router as image_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_device_id(request: Request, call_next):
    # Get device_id from header or generate new one
    device_id = request.headers.get("X-Device-ID")
    if not device_id:
        device_id = str(uuid.uuid4())
    
    # Add device_id to request state
    request.state.device_id = device_id
    
    response = await call_next(request)
    
    # Add device_id to response header if it was newly generated
    if not request.headers.get("X-Device-ID"):
        response.headers["X-Device-ID"] = device_id
    
    return response

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
    uvicorn.run(app, host="0.0.0.0", port=8080)
