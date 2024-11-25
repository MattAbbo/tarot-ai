# app/services/openai_service.py
import os
import uuid
import logging
from openai import OpenAI
from fastapi import HTTPException
from typing import Optional
from ..constants.ai_prompts import TAROT_READER_PROMPT
from .langfuse_service import langfuse_service

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        # Add detailed debug logging
        logger.debug("Environment variables:")
        for key in os.environ:
            if "KEY" in key:  # Only log names of key-related vars, not values
                logger.debug(f"Found env var: {key}")
        
        logger.debug(f"OpenAI API key found: {'yes' if api_key else 'no'}")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Log first few chars of key to verify format
        logger.debug(f"API Key starts with: {api_key[:7]}...")
        
        self.client = OpenAI(api_key=api_key)
        logger.debug("OpenAI client initialized")

    async def get_card_interpretation(self, card_name: str, context: Optional[str], reflection: str) -> dict:
        session_id = str(uuid.uuid4())
        try:
            logger.debug(f"=== Getting Card Interpretation ===")
            logger.debug(f"Card: {card_name}")
            logger.debug(f"Context: {context}")
            logger.debug(f"Reflection: {reflection}")

            user_prompt = f"""The card drawn is: {card_name}

Question/Context: {context if context else "No specific question asked"}
Querent's reflection: {reflection if reflection else "No specific reflection provided"}

Provide an interpretation for {card_name}, incorporating any insights shared."""

            logger.debug(f"User Prompt: {user_prompt}")

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": TAROT_READER_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            completion = response.choices[0].message.content
            logger.debug(f"OpenAI Response received: {completion[:100]}...")

            await langfuse_service.track_reading(
                session_id=session_id,
                reading_data={
                    "card_name": card_name,
                    "context": context,
                    "reflection": reflection,
                    "system_prompt": TAROT_READER_PROMPT,
                    "user_prompt": user_prompt,
                    "completion": completion,
                    "model": "gpt-3.5-turbo"
                }
            )
            
            return {
                "interpretation": completion,
                "session_id": session_id
            }
            
        except Exception as e:
            logger.error(f"OpenAI Error: {str(e)}")
            logger.exception("Full traceback:")
            await langfuse_service.track_error(
                session_id=session_id,
                error=str(e),
                context="card_interpretation"
            )
            raise HTTPException(
                status_code=500, 
                detail=str(e)
            )

openai_service = OpenAIService()