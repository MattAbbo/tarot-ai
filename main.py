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

# Card definitions
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
async def get_reading(request: ReadingRequest):
  try:
      print("Starting reading request with context:", request.context)

      # Pick random card
      card = random.choice(major_arcana + minor_arcana)
      print("Selected card:", card)

      # Get image
      try:
          print("Searching for card image...")
          with DDGS() as ddgs:
              urls = [
                  r['image']
                  for r in ddgs.images(f'Rider Waite {card} tarot card',
                                       max_results=10)
                  if 'i.pinimg.com' in r['image']
              ]
          print(f"Found {len(urls)} images")

          if not urls:
              print("No suitable images found")
              raise HTTPException(status_code=404,
                                  detail="No suitable image found")

      except Exception as e:
          print(f"Image search error: {str(e)}")
          raise HTTPException(status_code=500,
                              detail=f"Failed to search for image: {str(e)}")

      # Download image
      try:
          print("Downloading image...")
          with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp:
              download_url(urls[0], tmp.name, show_progress=False)
              with open(tmp.name, 'rb') as img_file:
                  img_data = base64.b64encode(img_file.read()).decode()
          print("Image downloaded and encoded successfully")

      except Exception as e:
          print(f"Image download error: {str(e)}")
          raise HTTPException(status_code=500,
                              detail=f"Failed to download image: {str(e)}")

      # Get interpretation
      try:
          print("Getting interpretation from OpenAI...")
          client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
          interpretation = client.chat.completions.create(
              model="gpt-4",
              messages=[{
                  "role":
                  "system",
                  "content":
                  """You are a knowledgeable tarot reader specializing in the Rider-Waite-Smith deck.
                  IMPORTANT: Keep total response under 1000 characters.
                  Interpret for the querent's context.
                  When interpreting, point out max 2 often-overlooked symbolic details in the card's imagery that are particularly relevant to the querent's situation."""
              }, {
                  "role":
                  "user",
                  "content":
                  f"Card drawn: '{card}'. Context from querent: '{request.context}'. Interpret this card specifically relating to their situation, highlighting often overlooked meaningful symbols in the card's artwork."
                  if request.context else
                  f"Interpret '{card}', including often-missed details from the Rider-Waite-Smith imagery. KEEP UNDER 1000 CHARACTERS."
              }],
              max_tokens=400
          ).choices[0].message.content
          print("Got interpretation from OpenAI")

      except Exception as e:
          print(f"OpenAI API error: {str(e)}")
          raise HTTPException(status_code=500,
                              detail=f"Failed to get interpretation: {str(e)}")

      # Prepare and send response
      print("Preparing response...")
      response_data = {
          "card_name": card,
          "image_data": f"data:image/jpeg;base64,{img_data}",
          "interpretation": interpretation
      }
      print("Response ready, sending...")
      return response_data

  except Exception as e:
      print(f"Unexpected error in get_reading: {str(e)}")
      raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8080)