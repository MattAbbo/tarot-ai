import os
import logging
from openai import OpenAI
from fastapi import HTTPException
from backend.app.constants.ai_prompts import TAROT_READER_PROMPT, IMAGE_INTERPRETER_PROMPT

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class OpenAIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)

    async def get_card_interpretation(self, card_name: str, context: str, reflection: str) -> str:
        try:
            question = context.split('CARD:')[0].strip() if "CARD:" in context else "No specific question"
            message_content = f"""The card drawn is: {card_name}

Original question: {question}
Querent's reflection: {reflection if reflection else "No specific reflection provided"}

Provide an interpretation for {card_name}, incorporating any insights shared."""
            
            logging.info(f"Request to OpenAI: Card chosen: {card_name}, Question asked: {question}, Reflection: {reflection}")

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Fixed model name
                messages=[
                    {"role": "system", "content": TAROT_READER_PROMPT},
                    {"role": "user", "content": message_content},
                ],
                max_tokens=400,
            )
            
            interpretation = response.choices[0].message.content
            logging.info(f"OpenAI Interpretation: {interpretation}")

            return interpretation
        except Exception as e:
            logging.error(f"OpenAI Error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to get interpretation: {str(e)}")

    async def interpret_image(self, encoded_image: str, context: str) -> str:
        try:
            user_message = [
                {"type": "text", "text": f"Context: {context}\n\nWhat spiritual insights can you derive from this image?"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
            ]
            
            logging.info(f"Request to OpenAI: Context: {context}, Image provided.")

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": IMAGE_INTERPRETER_PROMPT},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=400,
            )
            
            interpretation = response.choices[0].message.content
            logging.info(f"OpenAI Image Interpretation: {interpretation}")

            return interpretation
        except Exception as e:
            logging.error(f"OpenAI Error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to interpret image: {str(e)}")
