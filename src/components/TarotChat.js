const { useState, useRef, useEffect } = React;

// Ensure MESSAGES is available from window object
const MESSAGES = window.MESSAGES || {
    welcome: "Welcome to Tarot AI",
    error: "An error occurred",
    drawing: ["Drawing a card..."],
    loading: ["Loading..."]
};

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
    const [currentSessionId, setCurrentSessionId] = useState(null);
    const chatContainerRef = useRef(null);
    const fileInputRef = useRef(null);

    const scrollToLatestMessage = () => {
        if (chatContainerRef.current) {
            const messagesContainer = chatContainerRef.current.querySelector('.max-w-2xl');
            if (messagesContainer && messagesContainer.lastElementChild) {
                const lastMessage = messages[messages.length - 1];
                // Only scroll if the last message is not a card
                if (lastMessage && lastMessage.type !== 'card') {
                    messagesContainer.lastElementChild.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'start' 
                    });
                }
            }
        }
    };

    useEffect(() => {
        // Add a small delay to ensure DOM is updated
        const timeoutId = setTimeout(scrollToLatestMessage, 100);
        return () => clearTimeout(timeoutId);
    }, [messages]);

    const addDebugMessage = (message, type = 'ai') => {
        console.log('Debug:', message);
        setMessages(prev => [...prev, {
            id: Date.now().toString(),
            content: message,
            type: type
        }]);
    };

    const submitFeedback = async (score, feedback = '') => {
        if (!currentSessionId) return;

        try {
            const response = await fetch('/api/feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: currentSessionId,
                    score,
                    feedback
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to submit feedback');
            }
        } catch (error) {
            console.error('Error submitting feedback:', error);
        }
    };

    const handleImageUpload = async (event) => {
        const file = event.target.files[0];
        if (!file) {
            addDebugMessage("No file selected");
            return;
        }

        try {
            addDebugMessage(`Processing ${file.type} file: ${file.name}`);

            // Check if it's an image
            if (!file.type.startsWith('image/')) {
                addDebugMessage("Selected file is not an image");
                return;
            }

            // Create a new FormData instance
            const formData = new FormData();
            formData.append('image', file);
            formData.append('context', input.trim());

            // Process the image
            await handleImageInterpretation(formData);
        } catch (error) {
            console.error('Error in handleImageUpload:', error);
            addDebugMessage(`Error handling image: ${error.message}`);
        } finally {
            // Clear the input value to allow selecting the same file again
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }
        }
    };

    const handleImageInterpretation = async (formData) => {
        if (isLoading) {
            addDebugMessage("System is busy, please wait");
            return;
        }

        try {
            setIsLoading(true);
            addDebugMessage("Analyzing your image...");

            const response = await fetch('/api/interpret-image', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(`Server error: ${errorData.detail || response.statusText}`);
            }

            const data = await response.json();
            setCurrentSessionId(data.session_id);

            // Remove the "Analyzing" message and add the results
            setMessages(prev => [
                ...prev.filter(m => m.content !== "Analyzing your image..."),
                {
                    id: Date.now().toString(),
                    content: data.image_data,
                    type: 'image'
                },
                {
                    id: (Date.now() + 1).toString(),
                    content: data.interpretation,
                    type: 'ai'
                }
            ]);

            setInput('');
            setState('complete');
        } catch (error) {
            console.error('Error in handleImageInterpretation:', error);
            addDebugMessage(`Failed to interpret image: ${error.message}`);
        } finally {
            setIsLoading(false);
        }
    };

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

            // Safely access MESSAGES.drawing array
            const drawingMessages = MESSAGES.drawing || ["Drawing a card..."];
            const drawingMessage = drawingMessages[
                Math.floor(Math.random() * drawingMessages.length)
            ];
            
            setMessages(prev => [...prev, {
                id: Date.now().toString(),
                content: drawingMessage,
                type: 'ai'
            }]);

            await new Promise(resolve => setTimeout(resolve, 1500));

            const response = await fetch('/api/reading', {
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

            setCurrentSessionId(data.session_id);

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

            // Safely access MESSAGES.loading array
            const loadingMessages = MESSAGES.loading || ["Loading..."];
            const loadingMessage = loadingMessages[
                Math.floor(Math.random() * loadingMessages.length)
            ];
            
            setMessages(prev => [...prev, {
                id: Date.now().toString(),
                content: loadingMessage,
                type: 'ai'
            }]);

            const fullContext = `${currentCard.originalContext || ''} CARD: ${currentCard.name}`;

            const response = await fetch('/api/reading', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    context: fullContext,
                    reflection: userReflection || ' ',
                    session_id: currentSessionId
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

            // Submit positive feedback for successful reading
            await submitFeedback(1);

            setState('complete');
            setInput('');

        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, {
                id: Date.now().toString(),
                content: MESSAGES.error,
                type: 'ai'
            }]);
            // Submit negative feedback for failed reading
            await submitFeedback(0, error.message);
        } finally {
            setIsLoading(false);
        }
    };

    const startNewReading = () => {
        setState('initial');
        setCurrentCard(null);
        setCurrentSessionId(null);
        setInput('');
    };

    // Expose methods for DrawButton
    if (typeof window !== 'undefined') {
        window.TarotChat = window.TarotChat || {};
        window.TarotChat.handleImageUpload = handleImageUpload;
    }

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
                    {(currentState === 'initial' || currentState === 'reflection') && (
                        <InputSection 
                            value={input}
                            onChange={setInput}
                            onSubmit={handleInput}
                            state={currentState}
                            isLoading={isLoading}
                        />
                    )}
                    <DrawButton 
                        onClick={handleMainButton}
                        disabled={isLoading}
                        state={currentState}
                        fileInputRef={fileInputRef}
                    />
                </div>
            </div>
        </div>
    );
}

// Only expose to window if we're in a browser environment
if (typeof window !== 'undefined') {
    window.TarotChat = TarotChat;
}
