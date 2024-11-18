window.DrawButton = function DrawButton({ onClick, disabled, state }) {
    const getButtonText = () => {
        switch(state) {
            case 'reflection':
                return '🔮 Reveal Interpretation';
            case 'complete':
                return '✨ Draw New Card';
            default:
                return '✨ Draw Card';
        }
    };

    return (
        <button
            onClick={onClick}
            disabled={disabled}
            className={`bg-crystal-500 hover:bg-crystal-600 text-white px-6 py-2 rounded-lg font-medium transition-all
                ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
            {getButtonText()}
        </button>
    );
};