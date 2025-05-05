import socketio
import json
import os
from agent import choose_action, save_model

sio = socketio.Client()
log_file = "stats_collector/metrics.json"
os.makedirs(os.path.dirname(log_file), exist_ok=True)

@sio.event
def connect():
    print(" Connected to signaling server")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.on('stats')
def handle_stats(data):
    action = choose_action(data)
    data["action"] = action
    with open(log_file, 'a') as f:
        f.write(json.dumps(data) + "\n")
    sio.emit('rl-action', {'bitrate': action})

try:
    sio.connect('http://localhost:3000')
    sio.wait()
except KeyboardInterrupt:
    print(" Training interrupted. Saving Q-table...")
    save_model()
