import React, { useState, useRef, useEffect } from 'react';
import useMessages from '../hooks/useMessages';
import useCard from '../hooks/useCard';
import { MESSAGES } from '../constants/messages';

function TarotChat() {
  const { messages, addMessage, removeMessage } = useMessages(); // useMessages hook
  const { currentState, handleCardDraw, handleInterpretation, reset } = useCard(); // useCard hook
  const [isLoading, setIsLoading] = useState(false);
  const [input, setInput] = useState('');
  const chatContainerRef = useRef(null);

  const scrollToLatestMessage = () => {
    if (chatContainerRef.current) {
      const messagesContainer = chatContainerRef.current.querySelector('.max-w-2xl');
      if (messagesContainer && messagesContainer.lastElementChild) {
        messagesContainer.lastElementChild.scrollIntoView({
          behavior: 'smooth',
          block: 'start',
        });
      }
    }
  };

  useEffect(() => {
    const timeoutId = setTimeout(scrollToLatestMessage, 100);
    return () => clearTimeout(timeoutId);
  }, [messages]);

  const handleMainButton = async () => {
    if (isLoading) return;
    setIsLoading(true);

    try {
      switch (currentState) {
        case 'reflection':
          await handleInterpretation(input.trim(), addMessage, removeMessage);
          break;
        case 'complete':
          reset();
          await handleCardDraw('', addMessage, removeMessage);
          break;
        default:
          if (input.trim()) {
            addMessage(input.trim(), 'user');
          }
          await handleCardDraw(input.trim(), addMessage, removeMessage);
      }
      setInput('');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInput = () => {
    if (isLoading || !input.trim()) return;
    handleMainButton();
  };

  return (
    <div className="fixed inset-0 flex flex-col bg-mystic-900">
      <Header />
      <div className="flex-1 overflow-y-auto p-4" ref={chatContainerRef}>
        <div className="max-w-2xl mx-auto space-y-4">
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
        </div>
      </div>
      <div className="shrink-0 border-t border-purple-900 bg-mystic-900">
        <div className="max-w-2xl mx-auto p-4 space-y-4">
          <InputSection
            value={input}
            onChange={setInput}
            onSubmit={handleInput}
            state={currentState}
            isLoading={isLoading}
          />
          <DrawButton
            onClick={handleMainButton}
            disabled={isLoading}
            state={currentState}
          />
        </div>
      </div>
    </div>
  );
}

export default TarotChat;