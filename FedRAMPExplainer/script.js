const API_URL = 'http://localhost:5001/api/fedramp';

const input = document.getElementById('control-input');
const btn = document.getElementById('explain-btn');
const placeholder = document.getElementById('output-placeholder');
const content = document.getElementById('output-content');
const errorEl = document.getElementById('error-message');

input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') explain();
});

function selectChip(el, controlId) {
    document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
    el.classList.add('active');
    input.value = controlId;
    explain();
}

async function explain() {
    const controlId = input.value.trim().toUpperCase();
    if (!controlId) {
        input.focus();
        return;
    }

    setLoading(true);
    clearOutput();

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ control_id: controlId }),
        });

        if (!response.ok) {
            const err = await response.json().catch(() => ({}));
            throw new Error(err.error || `Server error: ${response.status}`);
        }

        content.classList.add('streaming');
        placeholder.classList.add('hidden');

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let accumulated = '';

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
                    content.innerHTML = marked.parse(accumulated);
                } catch (_) {}
            }
        }

        content.classList.remove('streaming');

    } catch (err) {
        showError(err.message);
    } finally {
        setLoading(false);
    }
}

function setLoading(loading) {
    btn.disabled = loading;
    btn.innerHTML = loading
        ? '<i class="fas fa-spinner fa-spin"></i> Thinking...'
        : '<i class="fas fa-search"></i> Explain';
}

function clearOutput() {
    content.innerHTML = '';
    content.classList.remove('streaming');
    errorEl.textContent = '';
    placeholder.classList.add('hidden');
}

function showError(msg) {
    placeholder.classList.add('hidden');
    content.innerHTML = '';
    errorEl.textContent = `Error: ${msg}. Make sure the backend is running (python fedramp_api.py).`;
}
