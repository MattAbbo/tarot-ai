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
        <div>
            <div className="flex items-center gap-2">
                <div className="relative flex-1">
                    <textarea
                        className="w-full bg-mystic-800 border-0 rounded-lg p-3 text-white placeholder-gray-400 focus:ring-1 focus:ring-crystal-500 resize-none"
                        placeholder={getPlaceholder()}
                        value={value}
                        onChange={(e) => {
                            const textarea = e.target;
                            textarea.style.height = 'auto';
                            textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
                            onChange(e.target.value);
                        }}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
                                e.preventDefault();
                                onSubmit();
                                e.target.style.height = 'auto';
                            }
                        }}
                        rows="1"
                        disabled={isLoading}
                    />
                </div>
            </div>
        </div>
    );
};
