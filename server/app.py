from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def home():
    return "WebSocket Chat Server is running!"

@socketio.on('message')
def handle_message(msg):
    print(f"Message received: {msg}")
    send(msg, broadcast=True)   # broadcast to all connected clients

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)  
