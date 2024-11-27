from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Serve the main chat page
@app.route('/')
def index():
    return render_template('index.html')

# Handle setting the username
@socketio.on('set_username')
def handle_set_username(username):
    print(f"User connected with username: {username}")
    emit('message', f"{username} has joined the chat!", broadcast=True)

# Handle incoming messages with username
@socketio.on('message')
def handle_message(data):
    username = data['username']
    msg = data['text']
    print(f"Message received from {username}: {msg}")
    emit('message', f"{username}: {msg}", broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

