const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export const fetchReading = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/reading`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching reading:', error);
    throw error;
  }
};

export const submitQuestion = async (question) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/draw-card`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    return await response.json();
  } catch (error) {
    console.error('Error submitting question:', error);
    throw error;
  }
};
