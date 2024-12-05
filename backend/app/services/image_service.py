# backend/app/services/image_service.py
import os
import base64
from fastapi import HTTPException
from backend.app.constants.cards import MAJOR_ARCANA_MAP, MINOR_ARCANA_MAP

class ImageService:
    def __init__(self):
        self.card_image_cache = {}
        # Get the path to the backend directory
        self.backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def get_card_image(self, card_name: str) -> str:
        """
        Retrieve a card image by name, using caching for performance.
        Returns base64 encoded image data.
        """
        if card_name in self.card_image_cache:
            return self.card_image_cache[card_name]

        try:
            filename = MAJOR_ARCANA_MAP.get(card_name) or MINOR_ARCANA_MAP.get(card_name)
            if not filename:
                raise ValueError(f"Invalid card name: {card_name}")

            # Use absolute path to the static directory inside backend
            image_path = os.path.join(self.backend_dir, 'static', 'cards', filename)
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found: {image_path}")

            with open(image_path, 'rb') as img_file:
                encoded = base64.b64encode(img_file.read()).decode()
                self.card_image_cache[card_name] = encoded
                return encoded

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading card image: {str(e)}")

    async def encode_image(self, image_content: bytes) -> str:
        """
        Encode image bytes to base64 string
        """
        try:
            return base64.b64encode(image_content).decode()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error encoding image: {str(e)}")
