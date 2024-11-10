document.addEventListener('DOMContentLoaded', function() {
    // Tab Funktionalität
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Entferne active class von allen tabs
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            // Füge active class zum geklickten tab hinzu
            btn.classList.add('active');
            document.getElementById(btn.dataset.tab).classList.add('active');
        });
    });

    // Chat Funktionalität
    const urlInput = document.getElementById('urlInput');
    const sendBtn = document.getElementById('sendBtn');
    const chatOutput = document.getElementById('chatOutput');

    sendBtn.addEventListener('click', async () => {
        const url = urlInput.value.trim();
        if (!url) return;

        // Füge User Message hinzu
        addMessage('user', url);

        try {
            const response = await fetch('/scrape', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            });

            const data = await response.json();
            addMessage('bot', formatScrapedData(data));
            
            // Füge zum Verlauf hinzu
            addToHistory(url, data);
        } catch (error) {
            addMessage('bot', 'Ein Fehler ist aufgetreten: ' + error.message);
        }

        urlInput.value = '';
    });

    function addMessage(type, content) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${type}-message`);
        messageDiv.textContent = content;
        chatOutput.appendChild(messageDiv);
        chatOutput.scrollTop = chatOutput.scrollHeight;
    }

    function formatScrapedData(data) {
        return `
            Titel: ${data.title}
            Beschreibung: ${data.description}
            Überschriften: ${data.headlines.join(', ')}
        `;
    }

    function addToHistory(url, data) {
        const historyList = document.getElementById('historyList');
        const historyItem = document.createElement('div');
        historyItem.classList.add('history-item');
        historyItem.innerHTML = `
            <p><strong>URL:</strong> ${url}</p>
            <p><strong>Zeit:</strong> ${new Date().toLocaleString()}</p>
        `;
        historyList.prepend(historyItem);
    }
}); 
