window.InputSection = function InputSection({ 
    value, 
    onChange, 
    onSubmit, 
    state,
    isLoading,
    onStartRecording,
    onStopRecording,
    onCancelRecording,
    isRecording,
    recordingTime 
}) {
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

    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    if (state === 'complete') return null;

    return (
        <div className="mt-4">
            {isRecording ? (
                <div className="flex items-center gap-2 bg-mystic-800 rounded-lg p-2">
                    <button
                        onClick={onCancelRecording}
                        className="text-red-500 hover:text-red-600 hover:bg-mystic-700 p-2 rounded-full"
                    >
                        <span className="block h-5 w-5">✕</span>
                    </button>
                    <div className="flex-1 flex items-center gap-2">
                        <div className="flex-1 h-4 bg-mystic-700 rounded-full overflow-hidden">
                            <div className="h-full bg-crystal-500 animate-pulse-custom rounded-full"></div>
                        </div>
                        <span className="text-sm text-gray-400 font-mono">
                            {formatTime(recordingTime)}
                        </span>
                    </div>
                    <button
                        onClick={onStopRecording}
                        className="text-crystal-500 hover:text-crystal-600 p-2 rounded-full"
                    >
                        <span className="block h-3 w-3 bg-current rounded-full"></span>
                    </button>
                </div>
            ) : (
                <div className="flex items-center gap-2">
                    <div className="relative flex-1">
                        <input
                            type="text"
                            className="w-full bg-mystic-800 border-0 rounded-lg p-3 pr-12 text-white placeholder-gray-400 focus:ring-1 focus:ring-crystal-500"
                            placeholder={getPlaceholder()}
                            value={value}
                            onChange={(e) => onChange(e.target.value)}
                            onKeyDown={handleKeyDown}
                            disabled={isLoading}
                        />
                        <button
                            onClick={onStartRecording}
                            disabled={isLoading}
                            className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-300 p-2"
                        >
                            <span className="block h-5 w-5">🎤</span>
                        </button>
                    </div>
                    <button
                        onClick={onSubmit}
                        disabled={isLoading}
                        className={`p-3 rounded-lg ${
                            isLoading ? 'bg-mystic-700' : 'bg-crystal-500 hover:bg-crystal-600'
                        }`}
                    >
                        <span className="block h-4 w-4">➤</span>
                    </button>
                </div>
            )}
        </div>
    );
};