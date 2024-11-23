# Tarot AI

An AI-powered Tarot reading application that combines traditional Tarot card interpretation with modern AI technology to provide personalized readings.

## Features

- Interactive Tarot card readings
- AI-powered interpretation using OpenAI's GPT models
- Complete Tarot deck visualization
- Chat interface for natural interaction
- eval system for reading quality

## Tech Stack

### Frontend
- React.js
- JavaScript
- Modern component architecture

### Backend
- Python
- FastAPI
- OpenAI API integration

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── constants/     # AI prompts and card definitions
│   │   ├── models/        # Data models
│   │   ├── routes/        # API endpoints
│   │   └── services/      # Business logic and external services
│   └── static/
│       └── cards/         # Tarot card images
├── src/
│   ├── components/        # React components
│   └── constants/         # Frontend constants
└── evals/                 # Evaluation system
    ├── src/              # Evaluation logic
    └── results/          # Evaluation reports
```

## Setup

1. Clone the repository

2. Install Python dependencies:
   ```bash
   poetry install
   ```

3. Install frontend dependencies:
   ```bash
   npm install
   ```

4. Configure environment variables:
   - Set up OpenAI API key
   - Configure other required environment variables

## Running the Application

1. Start the backend server:
   ```bash
   uvicorn backend.main:app --reload
   ```

2. Start the frontend development server:
   ```bash
   npm run dev
   ```

## Evaluation System

The project includes an evaluation system located in the `evals/` directory that:
- Assesses the quality of Tarot readings
- Generates analysis reports
- Provides metrics visualization
- Helps maintain reading consistency and accuracy

## Components

### Frontend Components
- TarotChat: Main chat interface for user interaction
- CardDisplay: Renders Tarot card images
- DrawButton: Handles card drawing mechanics
- InputSection: User input handling
- MessageBubble: Chat message display

### Backend Services
- OpenAI Service: Handles AI interpretation
- Reading Service: Core Tarot reading logic

## Development

The application is structured to separate concerns between frontend and backend:
- Frontend handles user interaction and display
- Backend manages AI integration, card logic, and data processing
- Evaluation system ensures reading quality

## License

MIT License
