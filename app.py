from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import subprocess

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

def start_serveo():
    """Start Serveo.net port forwarding and display the public URL."""
    try:
        print("Starting Serveo.net tunnel...")
        process = subprocess.Popen(
            ["ssh", "-R", "80:localhost:5000", "serveo.net"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        for line in iter(process.stdout.readline, ""):
            print(line.strip())
            if "Forwarding HTTP traffic from" in line:
                print(f"Public URL: {line.split(' ')[-1]}")
                break
    except Exception as e:
        print(f"Error starting Serveo tunnel: {e}")

if __name__ == '__main__':
    # Start the Serveo port forwarding
    start_serveo()

    # Run the Flask-SocketIO server
    socketio.run(app, host='0.0.0.0', port=5000)
