const { useState } = React;

function TarotChat() {
    const [messages, setMessages] = useState([{
        id: '1',
        content: MESSAGES.welcome,
        type: 'ai'
    }]);
    const [isLoading, setIsLoading] = useState(false);
    const [currentState, setState] = useState('initial');
    const [input, setInput] = useState('');
    const [currentCard, setCurrentCard] = useState(null);

    const handleMainButton = async () => {
        switch(currentState) {
            case 'reflection':
                await handleRevealInterpretation();
                break;
            case 'complete':
                startNewReading();
                break;
            default:
                await handleDrawCard();
        }
    };

    const handleInput = async () => {
        if (isLoading || !input.trim()) return;
        if (currentState === 'reflection') {
            await handleRevealInterpretation();
        } else {
            await handleDrawCard();
        }
    };

    const handleDrawCard = async () => {
        if (isLoading) return;
        
        try {
            setIsLoading(true);
            const userInput = input.trim();
            
            if (userInput) {
                setMessages(prev => [...prev, {
                    id: Date.now().toString(),
                    content: userInput,
                    type: 'user'
                }]);
            }

            const drawingMessage = MESSAGES.drawing[
                Math.floor(Math.random() * MESSAGES.drawing.length)
            ];
            
            setMessages(prev => [...prev, {
                id: Date.now().toString(),
                content: drawingMessage,
                type: 'ai'
            }]);

            await new Promise(resolve => setTimeout(resolve, 1500));

            const response = await fetch('/reading', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ context: userInput }),
            });

            if (!response.ok) throw new Error('Reading failed');
            const data = await response.json();
            
            setCurrentCard({
                name: data.card_name,
                image: data.image_data,
                originalContext: userInput
            });

            setMessages(prev => [
                ...prev.filter(m => m.content !== drawingMessage),
                {
                    id: Date.now().toString(),
                    content: data.card_name,
                    type: 'card',
                    card: {
                        name: data.card_name,
                        image: data.image_data
                    }
                },
                {
                    id: (Date.now() + 1).toString(),
                    content: data.reflection_prompt,
                    type: 'ai'
                }
            ]);

            setState('reflection');
            setInput('');
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, {
                id: Date.now().toString(),
                content: MESSAGES.error,
                type: 'ai'
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleRevealInterpretation = async () => {
        if (isLoading || !currentCard) return;

        try {
            setIsLoading(true);
            const userReflection = input.trim();
            
            if (userReflection) {
                setMessages(prev => [...prev, {
                    id: Date.now().toString(),
                    content: userReflection,
                    type: 'user'
                }]);
            }

            const loadingMessage = MESSAGES.loading[
                Math.floor(Math.random() * MESSAGES.loading.length)
            ];
            
            setMessages(prev => [...prev, {
                id: Date.now().toString(),
                content: loadingMessage,
                type: 'ai'
            }]);

            const fullContext = `${currentCard.originalContext || ''} CARD: ${currentCard.name}`;

            const response = await fetch('/reading', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    context: fullContext,
                    reflection: userReflection || ' '
                }),
            });

            if (!response.ok) throw new Error('Reading failed');
            const data = await response.json();
            
            setMessages(prev => {
                return prev.filter(m => m.content !== loadingMessage).concat({
                    id: Date.now().toString(),
                    content: data.interpretation,
                    type: 'ai'
                });
            });

            setState('complete');
            setInput('');

        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, {
                id: Date.now().toString(),
                content: MESSAGES.error,
                type: 'ai'
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    const startNewReading = () => {
        setState('initial');
        setCurrentCard(null);
        setInput('');
        setTimeout(() => handleDrawCard(), 0);
    };

    return (
        <div className="fixed inset-0 flex flex-col bg-mystic-900">
            <Header />
            <div className="flex-1 overflow-y-auto p-4">
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

window.TarotChat = TarotChat;
