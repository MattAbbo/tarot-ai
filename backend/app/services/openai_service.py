# app/services/openai_service.py
import os
import uuid
from openai import OpenAI
from fastapi import HTTPException
from typing import Optional
from ..constants.ai_prompts import TAROT_READER_PROMPT, IMAGE_INTERPRETER_PROMPT
from .langfuse_service import langfuse_service

class OpenAIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)

    async def get_card_interpretation(self, card_name: str, context: Optional[str], reflection: str) -> str:
        session_id = str(uuid.uuid4())
        try:
            user_prompt = f"""The card drawn is: {card_name}

Question/Context: {context if context else "No specific question asked"}
Querent's reflection: {reflection if reflection else "No specific reflection provided"}

Provide an interpretation for {card_name}, incorporating any insights shared."""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "system",
                    "content": TAROT_READER_PROMPT
                }, {
                    "role": "user",
                    "content": user_prompt
                }],
                max_tokens=400
            )
            
            completion = response.choices[0].message.content

            # Track interpretation with Langfuse
            langfuse_service.track_reading(
                session_id=session_id,
                reading_data={
                    "card_name": card_name,
                    "context": context,
                    "reflection": reflection,
                    "system_prompt": TAROT_READER_PROMPT,
                    "user_prompt": user_prompt,
                    "completion": completion,
                    "model": "gpt-4o-mini"
                }
            )
            
            return {
                "interpretation": completion,
                "session_id": session_id
            }
            
        except Exception as e:
            langfuse_service.track_error(
                session_id=session_id,
                error=str(e),
                context="card_interpretation"
            )
            print(f"OpenAI Error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to get interpretation: {str(e)}")

    async def interpret_image(self, encoded_image: str, context: str) -> str:
        session_id = str(uuid.uuid4())
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
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
            
            completion = response.choices[0].message.content

            # Track image interpretation with Langfuse
            langfuse_service.track_image_interpretation(
                session_id=session_id,
                interpretation_data={
                    "context": context,
                    "system_prompt": IMAGE_INTERPRETER_PROMPT,
                    "completion": completion,
                    "model": "gpt-4o-mini"
                }
            )
            
            return {
                "interpretation": completion,
                "session_id": session_id
            }
            
        except Exception as e:
            langfuse_service.track_error(
                session_id=session_id,
                error=str(e),
                context="image_interpretation"
            )
            print(f"OpenAI Error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to interpret image: {str(e)}")
