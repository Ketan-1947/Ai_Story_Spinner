// DOM elements
const urlInput = document.getElementById('urlInput');
const promptInput = document.getElementById('promptInput');
const processBtn = document.getElementById('processBtn');
const loading = document.getElementById('loading');
const messages = document.getElementById('messages');
const storyResults = document.getElementById('storyResults');
const originalStory = document.getElementById('originalStory');
const rewrittenStory = document.getElementById('rewrittenStory');
const submitEditBtn = document.getElementById('submitEditBtn');

// Main process button event listener
processBtn.addEventListener('click', async () => {
    const url = urlInput.value.trim();
    const prompt = promptInput.value.trim();
    
    if (!url) {
        showMessage('Please enter a valid URL', 'error');
        return;
    }

    setLoading(true);
    clearMessages();

    try {
        const formData = new FormData();
        formData.append('url', url);
        formData.append('prompt', prompt);

        const response = await fetch('/process_url', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            originalStory.value = data.original_content;
            rewrittenStory.value = data.rewritten_content;
            storyResults.style.display = 'block';
            showMessage('Story processed successfully!', 'success');
        } else {
            showMessage(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showMessage(`Network error: ${error.message}`, 'error');
    } finally {
        setLoading(false);
    }
});

// Helper functions
function setLoading(isLoading) {
    loading.style.display = isLoading ? 'block' : 'none';
    processBtn.disabled = isLoading;
    processBtn.textContent = isLoading ? 'Processing...' : 'Process Story';
}

function showMessage(message, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = type;
    messageDiv.textContent = message;
    messages.appendChild(messageDiv);
    
    // Auto-remove success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }
}

function clearMessages() {
    messages.innerHTML = '';
}

// Event listeners
urlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        processBtn.click();
    }
});

promptInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        processBtn.click();
    }
});

// Optional: Add some additional utility functions
function validateUrl(url) {
    try {
        new URL(url);
        return true;
    } catch (e) {
        return false;
    }
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showMessage('Text copied to clipboard!', 'success');
    }).catch(err => {
        showMessage('Failed to copy text', 'error');
    });
}

// You can extend this with more functionality as needed
console.log('AI Story Spinner initialized successfully!');

submitEditBtn.addEventListener('click', async () => {
    const original = originalStory.value;
    const rewritten = rewrittenStory.value; // This is the user-edited version
    const edited = rewrittenStory.value; // For now, treat the edited version as the current value

    setLoading(true);
    clearMessages();

    try {
        const formData = new FormData();
        formData.append('original', original);
        formData.append('rewritten', rewritten);
        formData.append('edited', edited);

        const response = await fetch('/submit_edit', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (data.message) {
            showMessage('Edit submitted successfully!', 'success');
        } else {
            showMessage('Failed to submit edit.', 'error');
        }
    } catch (error) {
        showMessage(`Network error: ${error.message}`, 'error');
    } finally {
        setLoading(false);
    }
});