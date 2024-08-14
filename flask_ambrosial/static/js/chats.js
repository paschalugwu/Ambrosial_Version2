document.addEventListener('DOMContentLoaded', function() {
    const socket = io.connect(window.location.protocol + "//" + window.location.host);

    const chatBox = document.getElementById('chat-box');
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');

    // Join the chat room
    socket.emit('join', {
        'username': '{{ username }}',
        'room': 'default'
    });

    // Listen for incoming messages
    socket.on('message', function(data) {
        const messageElement = document.createElement('div');
        const timestamp = new Date().toLocaleTimeString();

        if (data.msg.startsWith('{{ username }}:')) {
            messageElement.classList.add('text-right', 'bg-primary', 'text-white', 'rounded', 'p-2', 'mb-2');
            messageElement.style.maxWidth = '60%';
            messageElement.style.marginLeft = 'auto';
            messageElement.textContent = `[${timestamp}] ${data.msg}`;
        } else {
            messageElement.classList.add('text-left', 'bg-light', 'text-dark', 'rounded', 'p-2', 'mb-2');
            messageElement.style.maxWidth = '60%';
            messageElement.style.marginRight = 'auto';
            messageElement.textContent = `[${timestamp}] ${data.msg}`;
        }

        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the bottom
    });

    // Handle form submission
    chatForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const msg = messageInput.value;
        if (msg.trim() !== "") {
            socket.emit('message', {
                'username': '{{ username }}',
                'room': 'default',
                'msg': msg
            });

            // Clear the input field
            messageInput.value = '';
        }
    });
});
