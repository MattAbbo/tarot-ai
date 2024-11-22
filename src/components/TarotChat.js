const { useState, useRef, useEffect } = React;

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
    const chatContainerRef = useRef(null);
    const fileInputRef = useRef(null);

    const scrollToLatestMessage = () => {
        if (chatContainerRef.current) {
            const messagesContainer = chatContainerRef.current.querySelector('.max-w-2xl');
            if (messagesContainer && messagesContainer.lastElementChild) {
                messagesContainer.lastElementChild.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
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

            const response = await fetch('/interpret-image', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(`Server error: ${errorData.detail || response.statusText}`);
            }

            const data = await response.json();

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
    };

    // Expose methods for DrawButton
    window.TarotChat.handleImageUpload = handleImageUpload;

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
                        fileInputRef={fileInputRef}
                    />
                </div>
            </div>
        </div>
    );
}

window.TarotChat = TarotChat;
