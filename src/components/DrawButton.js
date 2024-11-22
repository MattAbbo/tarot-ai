function DrawButton({ onClick, disabled, state }) {
    const getButtonText = () => {
        switch(state) {
            case 'reflection':
                return 'Reveal Interpretation';
            case 'complete':
                return 'Start New Reading';
            default:
                return 'Draw a Card';
        }
    };

    return (
        <div className="flex flex-col items-center space-y-4">
            {state === 'initial' && (
                <div className="flex justify-center space-x-4 w-full">
                    <button
                        className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        onClick={onClick}
                        disabled={disabled}
                    >
                        {getButtonText()}
                    </button>
                    <button
                        className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        onClick={() => document.getElementById('imageUpload').click()}
                        disabled={disabled}
                    >
                        Upload Image
                    </button>
                    <input
                        type="file"
                        id="imageUpload"
                        accept=".jpg,.jpeg,.png,.gif,.webp"
                        className="hidden"
                        onChange={(e) => window.TarotChat.handleImageUpload(e)}
                    />
                </div>
            )}
            {state !== 'initial' && (
                <button
                    className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    onClick={onClick}
                    disabled={disabled}
                >
                    {getButtonText()}
                </button>
            )}
        </div>
    );
}

window.DrawButton = DrawButton;
