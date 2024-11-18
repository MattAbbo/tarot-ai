import React, { useState } from 'react';
import Header from './components/Header';
import CardDisplay from './components/CardDisplay';
import InputSection from './components/InputSection';
import DrawButton from './components/DrawButton';
import MessageBubble from './components/MessageBubble';
import { fetchReading } from './utils/api';
import './styles.css';

function App() {
  const [cards, setCards] = useState([]);
  const [reading, setReading] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleDrawCard = async () => {
    setIsLoading(true);
    try {
      const response = await fetchReading();
      setCards(response.cards);
      setReading(response.reading);
    } catch (error) {
      console.error('Error drawing cards:', error);
    }
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        <Header />
        <main className="mt-8">
          <CardDisplay cards={cards} />
          <DrawButton onClick={handleDrawCard} isLoading={isLoading} />
          {reading && <MessageBubble message={reading} />}
          <InputSection />
        </main>
      </div>
    </div>
  );
}

export default App;
