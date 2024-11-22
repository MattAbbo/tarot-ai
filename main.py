from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import random
from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
from pydantic import BaseModel
import tempfile
from fastapi.staticfiles import StaticFiles


# Load environment variables
load_dotenv()

# Add reflection prompts
REFLECTION_PROMPTS = [
    "What symbols in this card draw your attention?",
    "What emotions does this card stir within you?",
    "What story does this card tell you?",
    "What hidden messages do you see in the imagery?",
    "What energies do you feel emanating from this card?",
    "What details in this card speak directly to you?",
    "What deeper meaning reveals itself to you?",
    "What wisdom does this card hold for your situation?",
    "What patterns or symbols catch your eye?",
    "What aspects of your life does this card illuminate?",
    "How does this imagery connect to your inner journey?",
    "What memories or thoughts surface as you gaze at this card?",
    "What metaphors in this card resonate with your path?",
    "How does this card mirror your current experience?",
    "What secrets does this card whisper to your soul?",
    "How does this image reflect your deepest questions?",
    "What personal truth emerges from these symbols?",
    "How does this card speak to your present moment?",
    "What unconscious wisdom does this card reveal?",
    "How does this imagery dance with your intuition?",
    "What hidden aspects of yourself do you see reflected?",
    "How does this card challenge your perspective?",
    "What deeper understanding awaits in these symbols?",
    "How does this card illuminate your path forward?",
    "What unspoken message does this card hold for you?",
    "How does this imagery touch your inner knowing?",
    "What personal significance emerges from this card?",
    "How does this card reflect your spiritual journey?",
    "What subtle energies do you sense in this image?",
    "What transformative message lies within this card?"
]

# Add model for request validation
class ReadingRequest(BaseModel):
    context: str = ""  # Default empty string
    reflection: str = ""  # Add reflection field

# Check for API key early
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Check your .env file.")

# Initialize OpenAI client once
client = OpenAI(api_key=api_key)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/src", StaticFiles(directory="src"), name="src")

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

@app.post("/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    try:
        print("Received audio file for transcription")
        
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.filename)[1]) as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            # Use OpenAI's Whisper API to transcribe the audio
            print("Transcribing with Whisper...")
            with open(temp_file_path, "rb") as audio:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio,
                    response_format="text"
                )
            print("Transcription successful")

            # Clean up the temporary file
            os.unlink(temp_file_path)
            
            return {"transcription": transcript}

        except Exception as e:
            print(f"Transcription error: {str(e)}")
            # Clean up the temporary file in case of error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

    except Exception as e:
        print(f"Error in transcribe_audio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/interpret-image")
async def interpret_image(image: UploadFile = File(...), context: str = ""):
    try:
        print("Starting image interpretation")
        
        # Read and encode the image
        image_content = await image.read()
        
        # Convert to base64
        encoded_image = base64.b64encode(image_content).decode()
        
        # Get interpretation from OpenAI Vision API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are a thoughtful tarot reader. Analyze the image provided and give an intuitive reading.
                    Focus on:
                    - The symbolism and imagery present
                    - The emotions and energy it evokes
                    - How it might relate to the querent's situation
                    Keep your response under 1000 characters and maintain a contemplative tone."""
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
        
        interpretation = response.choices[0].message.content
        
        return {
            "interpretation": interpretation,
            "image_data": f"data:image/jpeg;base64,{encoded_image}"
        }
        
    except Exception as e:
        print(f"Error in interpret_image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reading")
async def get_reading(request: ReadingRequest):
    try:
        print("Starting reading request with context:", request.context)

        # If no reflection provided, draw a new card
        if not request.reflection:
            card = random.choice(all_cards)
            img_data = get_card_image(card)
            reflection_prompt = random.choice(REFLECTION_PROMPTS)
            
            return {
                "card_name": card,
                "image_data": f"data:image/jpeg;base64,{img_data}",
                "reflection_prompt": reflection_prompt
            }
        
        # If reflection is provided, generate the interpretation
        try:
            # Extract card name from context, with better error handling
            if "CARD:" not in request.context:
                print("Error: No card name found in context")
                return {
                    "interpretation": "I apologize, but I couldn't identify which card was drawn. Please try again."
                }
            
            card_name = request.context.split("CARD:")[1].strip()
            if not card_name:
                print("Error: Empty card name")
                return {
                    "interpretation": "I apologize, but I couldn't identify which card was drawn. Please try again."
                }

            # Validate that it's a real card
            if card_name not in all_cards:
                print(f"Error: Invalid card name: {card_name}")
                return {
                    "interpretation": "I apologize, but I couldn't identify the card. Please try again."
                }
            
            print(f"Interpreting card: {card_name}")
            interpretation = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "system",
                    "content": """You are a thoughtful tarot reader specializing in the Rider-Waite-Smith deck.
                        Balance your response between:
                        - 2-3 reflective questions about what the card asks of the querent
                        - 2-3 subtle insights based on their situation
                        - 1-2 often overlooked symbolic elements relevant to their context
                        
                        Keep total response under 1000 characters.
                        Consider both original question AND personal reflection if provided.
                        Stay nuanced and contemplative in tone."""
                }, {
                    "role": "user",
                    "content": f"""The card drawn is: {card_name}

Original question: {request.context.split('CARD:')[0].strip() if "CARD:" in request.context else "No specific question"}
Querent's reflection: {request.reflection if request.reflection else "No specific reflection provided"}

Provide an interpretation for {card_name}, incorporating any insights shared."""
                }],
                max_tokens=400
            ).choices[0].message.content
            print("Got interpretation from OpenAI")

            return {
                "interpretation": interpretation
            }

        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            return {
                "interpretation": "I apologize, but I couldn't complete the reading. Please try again."
            }

    except Exception as e:
        print(f"Error in get_reading: {str(e)}")
        return {
            "interpretation": "I apologize, but I couldn't complete the reading. Please try again."
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
