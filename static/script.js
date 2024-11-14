// Initial card image styling
const cardImage = document.getElementById('cardImage');
cardImage.style.maxWidth = '100%';
cardImage.style.height = 'auto';
cardImage.style.maxHeight = '70vh';

async function getReading() {
    console.log('Starting reading...');
    const context = document.getElementById('context').value || "";
    const drawButton = document.getElementById('drawCard');
    const loadingDiv = document.getElementById('loading');
    const readingDiv = document.getElementById('reading');
    const cardContainer = document.querySelector('.card-container');
    const shufflingText = document.querySelector('.shuffling-text');
    const cardBack = document.querySelector('.card-back');

    // Show loading state
    drawButton.disabled = true;
    cardContainer.classList.remove('hidden');
    readingDiv.classList.add('hidden');
    shufflingText.textContent = 'Consulting the stars...';
    console.log('Loading state shown');

    try {
        // Ensure minimum delay for the animation
        const minDelay = new Promise(resolve => setTimeout(resolve, 3000));

        const [response] = await Promise.all([
            fetch('/reading', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ context }),
            }),
            minDelay
        ]);

        console.log('Response received');
        const data = await response.json();
        console.log('Data parsed:', {
            cardName: data.card_name,
            hasImage: !!data.image_data
        });

        // Update content first
        document.getElementById('cardName').textContent = data.card_name;
        document.getElementById('interpretation').textContent = data.interpretation;

        console.log('Starting card transition');
        // Preload the new image
        const img = new Image();
        img.src = data.image_data;

        await new Promise((resolve) => {
            img.onload = () => {
                console.log('New image loaded');
                resolve();
            };
        });

        // First flip the card back
        cardBack.classList.add('flipping');
        console.log('Card back flipping');

        // Wait for flip
        await new Promise(resolve => setTimeout(resolve, 500));

        // Now show the new card
        console.log('Revealing new card');
        cardImage.src = data.image_data;
        cardImage.style.display = 'block';

        // Hide loading and show reading
        loadingDiv.classList.add('hidden');
        readingDiv.classList.remove('hidden');
        console.log('Transition complete');

    } catch (error) {
        console.error('Error during reading:', error);
        alert('Error getting reading. Please try again.');
    } finally {
        drawButton.disabled = false;
        if (!readingDiv.classList.contains('hidden')) {
            // Only reset if we successfully showed the reading
            shufflingText.textContent = 'Shuffling cards...';
            cardContainer.classList.add('hidden');
        }
    }
}