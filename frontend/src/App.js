import React, { useState } from 'react';
import Header from './components/Header';
import CardDisplay from './components/CardDisplay';
import InputSection from './components/InputSection';
import DrawButton from './components/DrawButton';
import MessageBubble from './components/MessageBubble';
import { fetchReading } from './utils/api';
import './styles.css';

function App() {
  // State management for cards, history, reading message, and loading status
  const [cardHistory, setCardHistory] = useState([]); // Stores all drawn cards
  const [currentCards, setCurrentCards] = useState([]); // Stores the cards from the latest draw
  const [reading, setReading] = useState(''); // Tarot reading message
  const [isLoading, setIsLoading] = useState(false); // Tracks loading state

  // Handles the "Draw New Card" button action
  const handleDrawCard = async () => {
    setIsLoading(true); // Set loading state
    try {
      // Call the API to fetch card data and a reading
      const response = await fetchReading();
      setCurrentCards(response.cards); // Update the cards for the current draw
      setCardHistory((prevHistory) => [...prevHistory, ...response.cards]); // Append to history
      setReading(response.reading); // Update the reading message
    } catch (error) {
      console.error('Error drawing cards:', error);
    }
    setIsLoading(false); // Reset loading state
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        {/* Header component */}
        <Header />
        <main className="mt-8">
          {/* Display the drawn cards */}
          <h2 className="text-xl font-bold">Current Draw</h2>
          <CardDisplay cards={currentCards} />
          
          {/* Display card history */}
          {cardHistory.length > 0 && (
            <div className="mt-6">
              <h2 className="text-xl font-bold">Card History</h2>
              <CardDisplay cards={cardHistory} />
            </div>
          )}
          
          {/* Button to draw new cards */}
          <DrawButton onClick={handleDrawCard} isLoading={isLoading} />
          
          {/* Display the reading message, if available */}
          {reading && (
            <div className="mt-4">
              <h2 className="text-xl font-bold">Reading</h2>
              <MessageBubble message={reading} />
            </div>
          )}
          
          {/* Input section for additional interactions */}
          <InputSection />
        </main>
      </div>
    </div>
  );
}

export default App;