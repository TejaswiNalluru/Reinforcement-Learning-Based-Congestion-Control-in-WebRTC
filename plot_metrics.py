import json
import matplotlib.pyplot as plt

file_path = "stats_collector/metrics.json"
data = []

with open(file_path, "r") as f:
    for line in f:
        try:
            data.append(json.loads(line.strip()))
        except json.JSONDecodeError:
            continue

timestamps = list(range(len(data)))
bitrates = [entry["bitrate"] / 1000 for entry in data]  # kbps
rtts = [entry["roundTripTime"] * 1000 for entry in data]  # ms
jitter = [entry["jitter"] * 1000 for entry in data]  # ms
loss = [entry.get("packetsLost", 0) for entry in data]
actions = [entry["action"] for entry in data]

plt.figure(figsize=(12, 6))
plt.plot(timestamps, bitrates, label="Bitrate (kbps)")
plt.plot(timestamps, rtts, label="RTT (ms)")
plt.plot(timestamps, jitter, label="Jitter (ms)")
plt.plot(timestamps, loss, label="Packet Loss")
plt.plot(timestamps, actions, label="Action (Set Bitrate)", linestyle="--")
plt.xlabel("Time (s)")
plt.ylabel("Value")
plt.title("QoE Metrics Over Time (RL Congestion Control)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
