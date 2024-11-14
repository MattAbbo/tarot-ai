// Initial setup
document.addEventListener('DOMContentLoaded', function() {
    const cardImage = document.getElementById('cardImage');
    cardImage.style.maxWidth = '100%';
    cardImage.style.height = 'auto';
    cardImage.style.maxHeight = '70vh';
    showPage('input-page');
});

function showPage(pageId) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => page.classList.add('hidden'));
    // Show requested page
    document.getElementById(pageId).classList.remove('hidden');
}

function startReading() {
    // Switch to reading page first
    showPage('reading-page');
    // Then start the reading process
    getReading();
}

function newReading() {
    // Clear previous inputs and states
    document.getElementById('context').value = '';
    document.getElementById('cardImage').style.display = 'none';
    const cardBack = document.querySelector('.card-back');
    if (cardBack) cardBack.classList.remove('flipping');

    // Return to input page
    showPage('input-page');
}

async function getReading() {
    const context = document.getElementById('context').value || "";
    const drawButton = document.getElementById('drawCard');

    try {
        // Ensure minimum delay for animation
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

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log('Response received:', {
            cardName: data.card_name,
            hasImage: !!data.image_data
        });

        // Update content
        document.getElementById('cardName').textContent = data.card_name;
        document.getElementById('interpretation').textContent = data.interpretation;

        // Handle image loading
        const img = new Image();
        img.onload = function() {
            const cardImage = document.getElementById('cardImage');
            cardImage.src = data.image_data;
            cardImage.style.display = 'block';
            showPage('result-page');
        };
        img.src = data.image_data;

    } catch (error) {
        console.error('Error:', error);
        alert('Error getting reading. Please try again.');
        showPage('input-page');
    }
}