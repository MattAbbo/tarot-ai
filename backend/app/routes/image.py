# src/routes/image.py
from fastapi import APIRouter, File, UploadFile
from ..services.openai_service import OpenAIService
from ..services.image_service import ImageService

router = APIRouter()
openai_service = OpenAIService()
image_service = ImageService()

@router.post("/interpret-image")
async def interpret_image(image: UploadFile = File(...), context: str = ""):
    image_content = await image.read()
    encoded_image = await image_service.encode_image(image_content)
    interpretation = await openai_service.interpret_image(encoded_image, context)
    
    return {
        "interpretation": interpretation,
        "image_data": f"data:image/jpeg;base64,{encoded_image}"
    }
