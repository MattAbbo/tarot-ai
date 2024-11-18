# Tarot AI

A modern web application that combines tarot card readings with AI-powered interpretations.

## Project Structure

```
project-root/
│
├── backend/             # Python backend
│   ├── app.py          # Main backend file
│   └── requirements.txt # Python dependencies
│
└── frontend/           # React frontend
    ├── public/
    │   └── index.html  # Entry point for React
    ├── src/
    │   ├── components/ # React components
    │   ├── utils/      # Utility functions
    │   ├── App.js      # Main React component
    │   ├── index.js    # React DOM entry
    │   └── styles.css  # Global styles
    ├── package.json    # Dependencies and scripts
    └── tailwind.config.js # Tailwind CSS config
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask server:
   ```bash
   python app.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The application will be available at `http://localhost:3000`

## Features

- Interactive tarot card drawing
- AI-powered card interpretations
- Real-time card display
- Responsive design
- Custom question input
- Modern UI with Tailwind CSS

## Technologies Used

- Frontend:
  - React
  - Tailwind CSS
  - Axios for API calls

- Backend:
  - Flask
  - Flask-CORS
  - Python

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License
