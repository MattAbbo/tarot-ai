const useCard = () => {
    const [currentCard, setCurrentCard] = useState(null);
    const [currentState, setState] = useState('initial');
  
    const handleCardDraw = async (userInput, addMessage, removeMessage) => {
      const drawingMessage = MESSAGES.drawing[Math.floor(Math.random() * MESSAGES.drawing.length)];
      addMessage(drawingMessage, 'ai');
  
      await new Promise(resolve => setTimeout(resolve, 1500));
      const data = await fetchCardReading(userInput);
  
      const newCard = {
        name: data.card_name,
        image: data.image_data,
        originalContext: userInput
      };
  
      setCurrentCard(newCard);
      removeMessage(drawingMessage);
      addMessage(data.card_name, 'card', { name: data.card_name, image: data.image_data });
      addMessage(data.reflection_prompt, 'ai');
      setState('reflection');
    };
  
    const handleInterpretation = async (userReflection, addMessage, removeMessage) => {
      if (!currentCard) return;
  
      const loadingMessage = MESSAGES.loading[Math.floor(Math.random() * MESSAGES.loading.length)];
      addMessage(loadingMessage, 'ai');
  
      const fullContext = `${currentCard.originalContext || ''} CARD: ${currentCard.name}`;
      const data = await fetchInterpretation(fullContext, userReflection);
  
      removeMessage(loadingMessage);
      addMessage(data.interpretation, 'ai');
      setState('complete');
    };
  
    const reset = () => {
      setState('initial');
      setCurrentCard(null);
    };
  
    return {
      currentCard,
      currentState,
      handleCardDraw,
      handleInterpretation,
      reset
    };
  };
  
  export default useCard;