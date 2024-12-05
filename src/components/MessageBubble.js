function MessageBubble({ message }) {
    const { type, content, card } = message;

    if (type === 'user') {
        return (
            <div className="flex justify-end">
                <div className="bg-purple-600 text-white rounded-lg px-4 py-2 max-w-[80%]">
                    {content}
                </div>
            </div>
        );
    }

    if (type === 'card' && card) {
        console.log('Card message data:', {
            type,
            card: {
                name: card.name,
                image: card.image
            }
        });

        // Add a fetch check for the image
        fetch(card.image)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                console.log('Image URL is accessible:', card.image);
            })
            .catch(error => {
                console.error('Image URL fetch error:', {
                    url: card.image,
                    error: error.message
                });
            });

        return (
            <div className="flex justify-start">
                <div className="bg-mystic-800 rounded-lg p-4 max-w-[80%]">
                    <h3 className="text-purple-300 font-medium mb-2">{card.name}</h3>
                    <img 
                        src={card.image} 
                        alt={card.name}
                        className="w-full max-w-sm mx-auto rounded-lg shadow-lg"
                        onError={(e) => {
                            console.error('Image load error:', {
                                src: e.target.src,
                                error: e.error,
                                currentSrc: e.target.currentSrc,
                                naturalWidth: e.target.naturalWidth,
                                naturalHeight: e.target.naturalHeight,
                                complete: e.target.complete,
                                readyState: e.target.readyState
                            });
                        }}
                        onLoad={(e) => {
                            console.log('Image loaded successfully:', {
                                src: card.image,
                                naturalWidth: e.target.naturalWidth,
                                naturalHeight: e.target.naturalHeight
                            });
                        }}
                    />
                </div>
            </div>
        );
    }

    if (type === 'image') {
        return (
            <div className="flex justify-start">
                <div className="bg-mystic-800 rounded-lg p-4 max-w-[80%]">
                    <img 
                        src={content} 
                        alt="Uploaded image"
                        className="w-full max-w-sm mx-auto rounded-lg shadow-lg"
                    />
                </div>
            </div>
        );
    }

    return (
        <div className="flex justify-start">
            <div className="bg-mystic-800 text-gray-100 rounded-lg px-4 py-2 max-w-[80%]">
                {content}
            </div>
        </div>
    );
}

window.MessageBubble = MessageBubble;
