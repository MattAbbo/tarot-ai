// Initial card image styling
const cardImage = document.getElementById('cardImage');
cardImage.style.maxWidth = '100%';
cardImage.style.height = 'auto';
cardImage.style.maxHeight = '70vh';

async function getReading() {
    const context = document.getElementById('context').value || "";
    const drawButton = document.getElementById('drawCard');
    const loadingDiv = document.getElementById('loading');
    const readingDiv = document.getElementById('reading');
    const cardContainer = document.querySelector('.card-container');
    const shufflingText = document.querySelector('.shuffling-text');

    // Show loading state
    drawButton.disabled = true;
    cardContainer.classList.remove('hidden');  // Show card back
    readingDiv.classList.add('hidden');

    // Change text to "Consulting the stars..."
    if (shufflingText) {
        shufflingText.textContent = 'Consulting the stars...';
    }

    try {
        const response = await fetch('/reading', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ context }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        // Update the UI with the reading
        document.getElementById('cardName').textContent = data.card_name;

        // Handle image loading
        const cardImage = document.getElementById('cardImage');
        cardImage.onload = function() {
            cardImage.style.display = 'block';
            readingDiv.classList.remove('hidden');
            loadingDiv.classList.add('hidden');
        };
        cardImage.src = data.image_data;

        document.getElementById('interpretation').textContent = data.interpretation;

    } catch (error) {
        console.error('Error:', error);
        alert('Error getting reading. Please try again.');
    } finally {
        // Hide loading, enable button
        drawButton.disabled = false;

        // Reset text back to "Shuffling cards..."
        if (shufflingText) {
            shufflingText.textContent = 'Shuffling cards...';
        }
    }
}