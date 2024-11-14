from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import random
from openai import OpenAI
import os
import base64
from pydantic import BaseModel

# Add model for request validation
class ReadingRequest(BaseModel):
    context: str = ""  # Default empty string

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pre-compute all card mappings
major_arcana_map = {
    'The Fool': '00-TheFool.jpg',
    'The Magician': '01-TheMagician.jpg',
    'The High Priestess': '02-TheHighPriestess.jpg',
    'The Empress': '03-TheEmpress.jpg',
    'The Emperor': '04-TheEmperor.jpg',
    'The Hierophant': '05-TheHierophant.jpg',
    'The Lovers': '06-TheLovers.jpg',
    'The Chariot': '07-TheChariot.jpg',
    'Strength': '08-Strength.jpg',
    'The Hermit': '09-TheHermit.jpg',
    'Wheel of Fortune': '10-WheelOfFortune.jpg',
    'Justice': '11-Justice.jpg',
    'The Hanged Man': '12-TheHangedMan.jpg',
    'Death': '13-Death.jpg',
    'Temperance': '14-Temperance.jpg',
    'The Devil': '15-TheDevil.jpg',
    'The Tower': '16-TheTower.jpg',
    'The Star': '17-TheStar.jpg',
    'The Moon': '18-TheMoon.jpg',
    'The Sun': '19-TheSun.jpg',
    'Judgement': '20-Judgement.jpg',
    'The World': '21-TheWorld.jpg'
}

# Pre-compute number mappings
number_map = {
    'Ace': '01', 'Two': '02', 'Three': '03', 'Four': '04', 'Five': '05',
    'Six': '06', 'Seven': '07', 'Eight': '08', 'Nine': '09', 'Ten': '10',
    'Page': '11', 'Knight': '12', 'Queen': '13', 'King': '14'
}

suits = ['Wands', 'Cups', 'Swords', 'Pentacles']
numbers = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten']
courts = ['Page', 'Knight', 'Queen', 'King']

# Pre-compute minor arcana mappings
minor_arcana_map = {}
for suit in suits:
    for value in numbers + courts:
        card_name = f"{value} of {suit}"
        filename = f"{suit}{number_map[value]}.jpg"
        minor_arcana_map[card_name] = filename

# Combine all card names for random selection
all_cards = list(major_arcana_map.keys()) + list(minor_arcana_map.keys())

# Cache for encoded images
card_image_cache = {}

def get_card_image(card_name: str) -> str:
    # Check cache first
    if card_name in card_image_cache:
        return card_image_cache[card_name]

    try:
        # Get filename from pre-computed mappings
        filename = major_arcana_map.get(card_name) or minor_arcana_map.get(card_name)
        if not filename:
            raise ValueError(f"Invalid card name: {card_name}")

        image_path = f'static/cards/{filename}'
        print(f"Loading image: {image_path}")

        if os.path.exists(image_path):
            with open(image_path, 'rb') as img_file:
                encoded = base64.b64encode(img_file.read()).decode()
                card_image_cache[card_name] = encoded
                return encoded
        else:
            raise FileNotFoundError(f"Image not found: {image_path}")

    except Exception as e:
        print(f"Error loading image: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading card image: {str(e)}")

@app.get("/")
async def read_root():
    return FileResponse('index.html')

@app.post("/reading")
async def get_reading(request: ReadingRequest):
    try:
        print("Starting reading request with context:", request.context)

        # Pick random card from pre-computed list
        card = random.choice(all_cards)
        print("Selected card:", card)

        # Get image from cache or load it
        print("Loading card image...")
        img_data = get_card_image(card)
        print("Image loaded successfully")

        # Get interpretation
        try:
            print("Getting interpretation from OpenAI...")
            client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
            interpretation = client.chat.completions.create(
                model="gpt-4",
                messages=[{
                    "role": "system",
                    "content": """You are a knowledgeable tarot reader specializing in the Rider-Waite-Smith deck.
                    IMPORTANT: Keep total response under 1000 characters.
                    Interpret for the querent's context.
                    When interpreting, point out max 2 often-overlooked symbolic details in the card's imagery that are particularly relevant to the querent's situation."""
                }, {
                    "role": "user",
                    "content": f"Card drawn: '{card}'. Context from querent: '{request.context}'. Interpret this card specifically relating to their situation, highlighting often overlooked meaningful symbols in the card's artwork."
                    if request.context else
                    f"Interpret '{card}', including often-missed details from the Rider-Waite-Smith imagery. KEEP UNDER 1000 CHARACTERS."
                }],
                max_tokens=400
            ).choices[0].message.content
            print("Got interpretation from OpenAI")

        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to get interpretation: {str(e)}")

        # Prepare and send response
        response_data = {
            "card_name": card,
            "image_data": f"data:image/jpeg;base64,{img_data}",
            "interpretation": interpretation
        }
        print("Response ready, sending...")
        return response_data

    except Exception as e:
        print(f"Error in get_reading: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)