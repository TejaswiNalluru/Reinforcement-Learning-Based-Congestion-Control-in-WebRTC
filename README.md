# Reinforcement-Learning-Based-Congestion-Control-in-WebRTC
#  RL-Based Congestion Control for WebRTC

This project implements a Reinforcement Learning (RL) based congestion control system for real-time video communication using WebRTC. Instead of using Google’s heuristic-based GCC (Google Congestion Control), this system uses a Q-learning agent to dynamically adapt bitrate based on live network metrics like RTT, jitter, and packet loss — improving overall Quality of Experience (QoE).

---

##  Features

- 📡 Real-time WebRTC video streaming between two browser clients
- 🤖 Python-based RL agent using Q-learning
- 🔁 Real-time metric exchange via WebSocket (Socket.IO)
- ⚙️ Adaptive bitrate control using `RTCRtpSender.setParameters()`
- 📊 QoE metrics logging and visualization
- 🧩 Modular architecture: front-end (HTML/JS), back-end (Node.js + Python)

---

## How to Run the Project

1. Start the Signaling Server  
   node server.js
2. Start the RL Agent Server  
   python rl_agent/socket_handler.py
3. Open WebRTC Clients  
   Open two browser tabs at: http://localhost:3000

## Visualize Results

After the video session ends, run:
  python plot_metrics.py
This generates line charts showing:
Actual bitrate (kbps)
RTT (ms)
Jitter (ms)
Packet Loss
Action bitrate decisions

## Sample Results
| Network | Avg. Bitrate (kbps) | RTT (ms) | Packet Loss (%) | Jitter (ms) |
| ------- | ------------------- | -------- | --------------- | ----------- |
| WiFi    | 2200                | 45       | 0.4             | 2.1         |
| 5G      | 3300                | 85       | 1.1             | 4.2         |
| LTE     | 1400                | 180      | 3.5             | 6.8         |

