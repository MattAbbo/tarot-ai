import React from 'react';

const CardDisplay = ({ cards }) => {
  if (!cards || cards.length === 0) {
    return null;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      {cards.map((card, index) => (
        <div key={index} className="relative">
          <img
            src={`/assets/cards/${card.image}`}
            alt={card.name}
            className="w-full rounded-lg shadow-lg transform transition-transform hover:scale-105"
          />
          <div className="absolute bottom-0 left-0 right-0 bg-black bg-opacity-70 p-2 rounded-b-lg">
            <h3 className="text-center text-white font-semibold">{card.name}</h3>
            {card.reversed && (
              <p className="text-center text-red-400 text-sm">Reversed</p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default CardDisplay;
