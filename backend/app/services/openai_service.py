0# app/services/openai_service.py
import os
from openai import OpenAI
from fastapi import HTTPException
from ..constants.ai_prompts import TAROT_READER_PROMPT, IMAGE_INTERPRETER_PROMPT

class OpenAIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)

    async def transcribe_audio(self, audio_file) -> str:
        try:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
            return transcript
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

    async def get_card_interpretation(self, card_name: str, context: str, reflection: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Fixed model name
                messages=[{
                    "role": "system",
                    "content": TAROT_READER_PROMPT
                }, {
                    "role": "user",
                    "content": f"""The card drawn is: {card_name}

Original question: {context.split('CARD:')[0].strip() if "CARD:" in context else "No specific question"}
Querent's reflection: {reflection if reflection else "No specific reflection provided"}

Provide an interpretation for {card_name}, incorporating any insights shared."""
                }],
                max_tokens=400
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI Error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to get interpretation: {str(e)}")

    async def interpret_image(self, encoded_image: str, context: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "system",
                        "content": IMAGE_INTERPRETER_PROMPT
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"Context: {context}\n\nWhat spiritual insights can you derive from this image?"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{encoded_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=400
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI Error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to interpret image: {str(e)}")
