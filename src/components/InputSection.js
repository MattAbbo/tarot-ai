window.InputSection = function InputSection({ 
    value, 
    onChange, 
    onSubmit, 
    state,
    isLoading
}) {
    React.useEffect(() => {
        if (window.lucide) {
            window.lucide.createIcons();
        }
    });

    const getPlaceholder = () => {
        if (state === 'reflection') {
            return "Share your reflection...";
        }
        return "Ask a question (optional)...";
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
            e.preventDefault();
            onSubmit();
        }
    };

    if (state === 'complete') return null;

    return (
        <div className="mt-4">
            <div className="flex items-center gap-2">
                <div className="relative flex-1">
                    <input
                        type="text"
                        className="w-full bg-mystic-800 border-0 rounded-lg p-3 pr-24 text-white placeholder-gray-400 focus:ring-1 focus:ring-crystal-500"
                        placeholder={getPlaceholder()}
                        value={value}
                        onChange={(e) => onChange(e.target.value)}
                        onKeyDown={handleKeyDown}
                        disabled={isLoading}
                    />
                    <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
                        <button
                            onClick={onSubmit}
                            disabled={isLoading || !value.trim()}
                            className={`p-2 rounded-md transition-colors ${
                                value.trim() ? 'text-crystal-500 hover:bg-mystic-700' : 'text-gray-600'
                            }`}
                        >
                            <i data-lucide="send" className="h-5 w-5"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};