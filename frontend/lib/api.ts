const API_URL = '/api/chat';

export async function askQuestion(question: string) {
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question }),
        });

        if (!response.ok) {
            throw new Error('Failed to fetch response');
        }

        return await response.json();
    } catch (error) {
        console.error("API Error:", error);
        return { answer: "Sorry, something went wrong connecting to the server." };
    }
}
