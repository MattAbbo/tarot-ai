# src/routes/audio.py
import os
import tempfile
from fastapi import APIRouter, File, UploadFile, HTTPException
from ..services.openai_service import OpenAIService

router = APIRouter()
openai_service = OpenAIService()

@router.post("/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.filename)[1]) as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            with open(temp_file_path, "rb") as audio:
                transcript = await openai_service.transcribe_audio(audio)
            
            os.unlink(temp_file_path)
            return {"transcription": transcript}

        except Exception as e:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
