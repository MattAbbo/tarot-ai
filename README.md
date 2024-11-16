# Tarot AI Reader 🔮

An AI-powered tarot reading application that combines traditional Rider-Waite-Smith tarot imagery with GPT-4 interpretations for personalized, interactive readings.

## Features

* 🎴 Single card readings with beautiful Rider-Waite-Smith imagery
* 🤖 GPT-4 powered interpretations highlighting card symbolism
* 🎙️ Voice input capability for questions and reflections
* 💭 Interactive reading flow with personal contemplation step
* 🎉 Smooth animations and transitions
* 💬 Modern chat-style interface
* 📱 Fully responsive design for all devices
* ⚡ Real-time typing animations for AI responses
* 🔄 Fallback mechanisms for API interruptions

## Demo

Visit [Live Demo](https://02b33366-89d7-4f71-b992-575a90a82e87-00-3a2ofplg3bx20.spock.replit.dev/)

## Reading Flow

1. **Ask Your Question**
   - Type your query or use voice input
   - Draw a card without a question for general guidance

2. **Card Reveal**
   - Watch as your card is revealed with smooth animations
   - See the traditional Rider-Waite-Smith artwork

3. **Personal Reflection**
   - Take time to contemplate the card's meaning
   - Share your own interpretation and insights

4. **AI Interpretation**
   - Receive a personalized interpretation that considers:
     - Your original question
     - The drawn card's symbolism
     - Your personal reflections

## Tech Stack

* **Frontend:**
  - HTML5, CSS3, JavaScript
  - React (via CDN)
  - Tailwind CSS
  - Lucide Icons

* **Backend:**
  - Python 3.13
  - FastAPI
  - OpenAI API (GPT-4 & Whisper)

* **APIs:**
  - OpenAI Chat Completion API for interpretations
  - OpenAI Whisper API for voice transcription

* **Deployment:**
  - Replit

## Local Development

1. Clone the repository
```bash
git clone https://github.com/yourusername/tarot-ai.git
cd tarot-ai
```

2. Set up Python environment with Poetry
```bash
poetry install
```

3. Create `.env` file
```env
OPENAI_API_KEY=your_key_here
```

4. Run the development server
```bash
poetry run uvicorn main:app --reload
```

The app will be available at `http://localhost:8000`

## Features in Development

- Multiple card spreads
- Reading history
- Sharing capabilities
- Account system
- Additional deck options

## Credits

* Rider-Waite-Smith Tarot imagery
* OpenAI GPT-4 & Whisper APIs
* FastAPI framework
* React & Tailwind CSS
* Lucide Icons

## License

Distributed under the MIT License. See `LICENSE` for more information.
