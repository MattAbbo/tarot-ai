from PIL import Image
from io import BytesIO
import os
import uuid
import logging
import base64
from openai import OpenAI
from fastapi import HTTPException
from typing import Optional
from ..constants.ai_prompts import TAROT_READER_PROMPT, IMAGE_INTERPRETER_PROMPT
from .langfuse_service import langfuse_service


# Set OpenAI client logging to WARNING level to suppress debug logs
logging.getLogger("openai").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        logger.debug("Environment variables:")
        for key in os.environ:
            if "KEY" in key:
                logger.debug(f"Found env var: {key}")
        
        logger.debug(f"OpenAI API key found: {'yes' if api_key else 'no'}")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        logger.debug(f"API Key starts with: {api_key[:7]}...")
        
        self.client = OpenAI(api_key=api_key)
        logger.debug("OpenAI client initialized")
        
    def resize_and_encode_image(self, image_path: str, max_size=(500, 500)) -> str:
        """
        Resize the image to a maximum size and encode it as a Base64 string.
        """
        try:
            logger.debug(f"Resizing image: {image_path} to max size {max_size}")
            img = Image.open(image_path)
            img.thumbnail(max_size)  # Resize the image
            buffer = BytesIO()
            img.save(buffer, format="JPEG")  # Save as JPEG to the buffer
            buffer.seek(0)
            encoded_image = base64.b64encode(buffer.read()).decode("utf-8")
            logger.debug(f"Image resized and encoded. Length of Base64 string: {len(encoded_image)}")
            return encoded_image
        except Exception as e:
            logger.error(f"Failed to resize and encode image: {str(e)}")
            raise HTTPException(status_code=500, detail="Image processing failed")

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
                model="gpt-4o-mini",
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
                    "model": "gpt-4o-mini"
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
            raise HTTPException(status_code=500, detail=str(e))

    async def interpret_image(self, encoded_image: str, context: str) -> str:
        try:
            """
            Interpret an image with context by resizing it and sending it to the API.
            """
            # Resize and encode the image
            encoded_image = self.resize_and_encode_image(image_path)

            # Construct the user message
            user_message = (
                f"Context: {context}\n\n"
                "What spiritual insights can you derive from this image?\n\n"
                f"![Image](data:image/jpeg;base64,{encoded_image})"
            )

            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": IMAGE_INTERPRETER_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=400
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"OpenAI Image Interpretation Error: {str(e)}")
            logger.exception("Full traceback:")
            raise HTTPException(status_code=500, detail=f"Failed to interpret image: {str(e)}")

openai_service = OpenAIService()
