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
            className={`w-full bg-crystal-500 hover:bg-crystal-600 text-white px-6 py-3 
                rounded-lg transition-all text-center text-lg
                ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
            {getButtonText()}
        </button>
    );
};