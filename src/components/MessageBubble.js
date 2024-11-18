// MessageBubble.js
window.MessageBubble = function MessageBubble({ message }) {
    return (
        <div
            className={`flex gap-2 ${
                message.type === 'user' ? 'justify-end' : 'justify-start'
            }`}
        >
            <div
                className={`rounded-lg p-4 max-w-[80%] ${
                    message.type === 'user'
                        ? 'bg-crystal-500'
                        : message.type === 'card'
                        ? 'bg-mystic-700'
                        : 'bg-mystic-800'
                }`}
            >
                {message.card && (
                    <div className="mb-4">
                        <h3 className="text-xl font-semibold mb-2 text-crystal-500 font-cinzel">
                            {message.card.name}
                        </h3>
                        <img
                            src={message.card.image}
                            alt={message.card.name}
                            className="rounded-lg mb-2 w-full max-w-[240px] mx-auto shadow-lg"
                        />
                    </div>
                )}
                <p className="text-sm text-white whitespace-pre-line">{message.content}</p>
            </div>
        </div>
    );
};