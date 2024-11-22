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

    if (type === 'card') {
        return (
            <div className="flex justify-start">
                <div className="bg-mystic-800 rounded-lg p-4 max-w-[80%]">
                    <h3 className="text-purple-300 font-medium mb-2">{card.name}</h3>
                    <img 
                        src={card.image} 
                        alt={card.name}
                        className="w-full max-w-sm mx-auto rounded-lg shadow-lg"
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
