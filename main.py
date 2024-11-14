from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import random
from openai import OpenAI
import os
from duckduckgo_search import DDGS
import base64
from fastdownload import download_url
import tempfile
from pydantic import BaseModel


# Add model for request validation
class ReadingRequest(BaseModel):
    context: str = ""  # Default empty string


app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Card definitions (keeping your original definitions)
major_arcana = [
    'The Fool', 'The Magician', 'The High Priestess', 'The Empress',
    'The Emperor', 'The Hierophant', 'The Lovers', 'The Chariot', 'Strength',
    'The Hermit', 'Wheel of Fortune', 'Justice', 'The Hanged Man', 'Death',
    'Temperance', 'The Devil', 'The Tower', 'The Star', 'The Moon', 'The Sun',
    'Judgement', 'The World'
]

suits = ['Wands', 'Cups', 'Swords', 'Pentacles']
numbers = [
    'Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
    'Ten'
]
courts = ['Page', 'Knight', 'Queen', 'King']
minor_arcana = [
    f"{num} of {suit}" for suit in suits for num in numbers + courts
]


@app.get("/")
async def read_root():
    return FileResponse('index.html')


@app.post("/reading")
async def get_reading(
        request: ReadingRequest):  # Changed to use Pydantic model
    try:
        # Pick random card
        card = random.choice(major_arcana + minor_arcana)

        # Get image with better error handling
        try:
            with DDGS() as ddgs:
                urls = [
                    r['image']
                    for r in ddgs.images(f'Rider Waite {card} tarot card',
                                         max_results=10)
                    if 'i.pinimg.com' in r['image']
                ]

            if not urls:
                raise HTTPException(status_code=404,
                                    detail="No suitable image found")

        except Exception as e:
            print(f"Image search error: {e}")
            raise HTTPException(status_code=500,
                                detail="Failed to search for image")

        # Download image with error handling
        try:
            with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp:
                download_url(urls[0], tmp.name, show_progress=False)
                with open(tmp.name, 'rb') as img_file:
                    img_data = base64.b64encode(img_file.read()).decode()
        except Exception as e:
            print(f"Image download error: {e}")
            raise HTTPException(status_code=500,
                                detail="Failed to download image")

        # Get interpretation (keeping your original prompt)
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
            max_tokens=400  # Increased to allow for 1000 characters
        ).choices[0].message.content

        return {
            "card_name": card,
            "image_data": f"data:image/jpeg;base64,{img_data}",
            "interpretation": interpretation
        }

    except Exception as e:
        print(f"Error in get_reading: {e}")  # Added logging
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
