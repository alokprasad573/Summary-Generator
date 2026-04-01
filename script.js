document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('summarization-form');
    const dialogueInput = document.getElementById('dialogue');
    const summarizeBtn = document.getElementById('summarize-btn');
    const summaryText = document.getElementById('summary-text');

    form.addEventListener('submit', async (e) => {
        // Prevent the page from refreshing on form submit
        e.preventDefault();

        const dialogueValue = dialogueInput.value.trim();
        if (!dialogueValue) return;

        // Visual Feedback: Update button state
        summarizeBtn.disabled = true;
        summarizeBtn.innerText = "Summarizing... ✨";
        summaryText.innerText = "Processing your request, please wait...";
        summaryText.classList.remove('text-red-600');
        summaryText.classList.add('text-gray-700');

        try {
            // POST request to FastAPI endpoint
            const response = await fetch('/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    dialogue: dialogueValue
                }),
            });

            // Check if the server returned a success status (200-299)
            if (!response.ok) {
                throw new Error(`Server Error: ${response.status} ${response.statusText}`);
            }

            const data = await response.json();

            // Display the generated summary
            summaryText.innerText = data.summary;

        } catch (error) {
            // Runtime Error Handling
            console.error("Summarization Error:", error);
            summaryText.innerText = "Oops! Something went wrong while generating the summary. Please check your connection and try again.";
            summaryText.classList.remove('text-gray-700');
            summaryText.classList.add('text-red-600');
            
        } finally {
            // Reset button state regardless of success or failure
            summarizeBtn.disabled = false;
            summarizeBtn.innerText = "Summarize 🚀";
        }
    });
});