let username = '';  // To store the username

// Establish a connection to the server using Socket.IO
const socket = io();

// Get references to the DOM elements
const messages = document.getElementById('messages');
const input = document.getElementById('message');
const usernameInput = document.getElementById('username');
const chatRoom = document.getElementById('chat-room');
const usernameContainer = document.getElementById('username-container');

// Function to set the username and show the chat room
function setUsername() {
    username = usernameInput.value.trim();
    if (username) {
        usernameContainer.style.display = 'none';  // Hide username input
        chatRoom.style.display = 'block';           // Show chat room
        socket.emit('set_username', username);     // Send username to server
    }
}

// Display incoming messages with the username
socket.on('message', function(msg) {
    const div = document.createElement('div');
    div.textContent = msg;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
});

// Function to send a message
function sendMessage() {
    if (input.value.trim()) {
        socket.emit('message', { username, text: input.value });  // Send message with username
        input.value = '';  // Clear the input field
    }
}

// Allow the user to press Enter to send a message
input.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

