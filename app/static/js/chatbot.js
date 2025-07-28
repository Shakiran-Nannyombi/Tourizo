function toggleChat() {
    const chatWindow = document.getElementById('chatWindow');
    chatWindow.style.display = chatWindow.style.display === 'none' ? 'block' : 'none';
}

let isWaiting = false;

function sendMessage() {
    if (isWaiting) return;
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    if (!message) return;
    appendMessage('You', message);
    input.value = '';
    isWaiting = true;
    showLoading();
    fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message})
    })
    .then(res => res.json())
    .then(data => {
        hideLoading();
        appendMessage('Tourizo AI', data.response);
    })
    .catch(() => {
        hideLoading();
        appendMessage('Tourizo AI', '<span style="color:red;">Sorry, there was an error.</span>');
    })
    .finally(() => {
        isWaiting = false;
    });
}

function showLoading() {
    const messages = document.getElementById('chatMessages');
    let loading = document.createElement('div');
    loading.id = 'chatLoading';
    loading.innerHTML = '<em>Tourizo AI is typing...</em>';
    loading.style.color = '#888';
    loading.style.margin = '8px 0';
    messages.appendChild(loading);
    messages.scrollTop = messages.scrollHeight;
}

function hideLoading() {
    const loading = document.getElementById('chatLoading');
    if (loading) loading.remove();
}

function appendMessage(sender, text) {
    const messages = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.innerHTML = `<strong>${sender}:</strong> ${text}`;
    div.style.margin = '8px 0';
    div.style.padding = '6px 10px';
    div.style.borderRadius = '8px';
    div.style.background = sender === 'You' ? '#e9f7fd' : '#f4f4f4';
    div.style.color = 'black';
    div.style.alignSelf = sender === 'You' ? 'flex-end' : 'flex-start';
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}

document.getElementById('chatInput').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') sendMessage();
});