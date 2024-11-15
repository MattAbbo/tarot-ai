# Tarot AI Reader 🔮

An AI-powered tarot reading application that combines traditional Rider-Waite-Smith tarot imagery with GPT-4 interpretations for personalized readings.

## Features
- Context-aware tarot readings
- Traditional Rider-Waite-Smith card imagery
- GPT-4 powered interpretations highlighting subtle card symbolism
- Smooth card reveal animations
- Mobile-responsive design

## Demo
https://02b33366-89d7-4f71-b992-575a90a82e87-00-3a2ofplg3bx20.spock.replit.dev/

## Tech Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python (FastAPI)
- AI: OpenAI GPT-4
- Image Processing: Local card image storage
- Deployment: Replit

## Local Development

1. Clone the repository
```bash
git clone https://github.com/yourusername/tarot-ai.git
cd tarot-ai
```

2. Set up Python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install fastapi uvicorn python-dotenv openai
```

4. Create `.env` file
```
OPENAI_API_KEY=your_key_here
```

5. Run the development server
```bash
uvicorn main:app --reload
```

The app will be available at `http://localhost:8000`

## Credits
- Rider-Waite-Smith Tarot imagery
- OpenAI GPT-4 API
- FastAPI framework

## License
Distributed under the MIT License. See `LICENSE` for more information.
