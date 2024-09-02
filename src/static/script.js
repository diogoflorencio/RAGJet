document.getElementById('send-button').addEventListener('click', sendMessage);
document.getElementById('chat-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Evita uma nova linha no input
        sendMessage();
    }
});

function sendMessage() {
    const chatInput = document.getElementById('chat-input');
    const messageText = chatInput.value.trim();

    if (messageText !== '') {
        const chatBox = document.getElementById('chat-box');
        const userMessage = document.createElement('div');
        userMessage.classList.add('chat-message', 'sent');
        userMessage.textContent = messageText;
        chatBox.appendChild(userMessage);

        chatInput.value = '';
        chatBox.scrollTop = chatBox.scrollHeight;

        simulateTypingIndicator(chatBox, messageText);
    }
}

function simulateTypingIndicator(chatBox, messageText) {
    const typingIndicator = document.createElement('div');
    typingIndicator.classList.add('chat-message', 'received');
    typingIndicator.innerHTML = '<div class="dot-typing"><div></div><div></div><div></div></div>';
    chatBox.appendChild(typingIndicator);
    chatBox.scrollTop = chatBox.scrollHeight;

    // request to the server rout post /form
    fetch('/form', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: messageText }) // Envia a mensagem como JSON
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro na requisição ao backend.');
        }
        return response.json();
    })
    .then(data => {
        // Remove o indicador de digitação
        typingIndicator.remove();

        // Exibe a resposta do backend
        const receivedMessage = document.createElement('div');
        receivedMessage.classList.add('chat-message', 'received');
        receivedMessage.textContent = data.response; // Resposta recebida do backend
        chatBox.appendChild(receivedMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        typingIndicator.remove();
        console.error('Erro:', error);

        // Exibe uma mensagem de erro no chat
        const errorMessage = document.createElement('div');
        errorMessage.classList.add('chat-message', 'received');
        errorMessage.textContent = 'Ocorreu um erro ao tentar enviar a mensagem.';
        chatBox.appendChild(errorMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}
