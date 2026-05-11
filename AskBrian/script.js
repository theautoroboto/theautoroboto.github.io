const API_URL = 'https://theautoroboto-github-io-1.onrender.com/api/ask';

const messagesEl = document.getElementById('messages');
const inputEl = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const suggestionsEl = document.getElementById('suggestions');

// Conversation history sent to the API (excludes the hardcoded welcome message)
const history = [];

// Auto-resize textarea
inputEl.addEventListener('input', () => {
    inputEl.style.height = 'auto';
    inputEl.style.height = Math.min(inputEl.scrollHeight, 120) + 'px';
});

inputEl.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

function sendSuggestion(el) {
    inputEl.value = el.textContent;
    suggestionsEl.classList.add('hidden');
    sendMessage();
}

async function sendMessage() {
    const text = inputEl.value.trim();
    if (!text || sendBtn.disabled) return;

    inputEl.value = '';
    inputEl.style.height = 'auto';
    suggestionsEl.classList.add('hidden');

    appendMessage('user', text);
    history.push({ role: 'user', content: text });

    setLoading(true);
    const assistantBubble = appendStreamingMessage();

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ messages: history }),
        });

        if (!response.ok) {
            const err = await response.json().catch(() => ({}));
            throw new Error(err.error || `Server error ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let accumulated = '';
        let updateScheduled = false;

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop();

            for (const line of lines) {
                if (!line.startsWith('data: ')) continue;
                const data = line.slice(6);
                if (data === '[DONE]') continue;

                try {
                    const parsed = JSON.parse(data);
                    accumulated += parsed.text;

                    if (!updateScheduled) {
                        updateScheduled = true;
                        requestAnimationFrame(() => {
                            assistantBubble.innerHTML = DOMPurify.sanitize(marked.parse(accumulated));
                            scrollToBottom();
                            updateScheduled = false;
                        });
                    }
                } catch (_) {}
            }
        }

        // Ensure the final state is rendered after the stream ends
        assistantBubble.innerHTML = DOMPurify.sanitize(marked.parse(accumulated));
        scrollToBottom();

        assistantBubble.classList.remove('streaming');
        history.push({ role: 'assistant', content: accumulated });

    } catch (err) {
        assistantBubble.classList.remove('streaming');
        assistantBubble.classList.add('error');
        assistantBubble.textContent = `Couldn't reach the backend. Make sure api/app.py is running (python api/app.py). Error: ${err.message}`;
        history.pop(); // remove the user message so conversation stays coherent
    } finally {
        setLoading(false);
    }
}

function appendMessage(role, text) {
    const msg = document.createElement('div');
    msg.className = `message ${role}`;
    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.textContent = text;
    msg.appendChild(bubble);
    messagesEl.appendChild(msg);
    scrollToBottom();
    return bubble;
}

function appendStreamingMessage() {
    const msg = document.createElement('div');
    msg.className = 'message assistant';
    const bubble = document.createElement('div');
    bubble.className = 'bubble streaming';
    bubble.innerHTML = '<div class="typing-dots"><span></span><span></span><span></span></div>';
    msg.appendChild(bubble);
    messagesEl.appendChild(msg);
    scrollToBottom();
    return bubble;
}

function setLoading(loading) {
    sendBtn.disabled = loading;
    inputEl.disabled = loading;
}

function scrollToBottom() {
    messagesEl.scrollTop = messagesEl.scrollHeight;
}
