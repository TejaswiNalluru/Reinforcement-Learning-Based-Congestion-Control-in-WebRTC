import numpy as np
import pickle
import os

bitrate_levels = [300, 500, 800, 1200]  # kbps
q_table_file = "models/q_table.pkl"

def discretize(value, bins):
    return np.digitize([value], bins)[0]

rtt_bins = [100, 200, 300, 500]
loss_bins = [0, 10, 30, 50]
jitter_bins = [10, 30, 60, 100]

num_states = (len(rtt_bins)+1)*(len(loss_bins)+1)*(len(jitter_bins)+1)*len(bitrate_levels)
num_actions = len(bitrate_levels)

if os.path.exists(q_table_file):
    with open(q_table_file, 'rb') as f:
        q_table = pickle.load(f)
else:
    q_table = np.zeros((num_states, num_actions))

alpha = 0.1
gamma = 0.9
epsilon = 0.1

prev_state = None
prev_action = None

def encode_state(rtt, loss, jitter, bitrate_idx):
    rtt_bin = discretize(rtt * 1000, rtt_bins)
    loss_bin = discretize(loss, loss_bins)
    jitter_bin = discretize(jitter * 1000, jitter_bins)
    return int((((rtt_bin*(len(loss_bins)+1)+loss_bin)*(len(jitter_bins)+1)+jitter_bin)*len(bitrate_levels))+bitrate_idx)

def compute_reward(bitrate, rtt, loss, jitter):
    return bitrate - (10*rtt*1000 + 5*loss + 3*jitter*1000)

def choose_action(state_features):
    global prev_state, prev_action

    rtt = state_features.get("roundTripTime", 0)
    loss = state_features.get("packetsLost", 0)
    jitter = state_features.get("jitter", 0)
    bitrate = state_features.get("bitrate", 800000) / 1000

    bitrate_index = min(range(len(bitrate_levels)), key=lambda i: abs(bitrate_levels[i] - bitrate))
    current_state = encode_state(rtt, loss, jitter, bitrate_index)

    # ε-greedy action
    if np.random.rand() < epsilon:
        action = np.random.randint(num_actions)
    else:
        action = np.argmax(q_table[current_state])

    # Q-learning update
    if prev_state is not None and prev_action is not None:
        reward = compute_reward(bitrate, rtt, loss, jitter)
        old_value = q_table[prev_state][prev_action]
        next_max = np.max(q_table[current_state])
        q_table[prev_state][prev_action] = old_value + alpha * (reward + gamma * next_max - old_value)

    prev_state = current_state
    prev_action = action

    return bitrate_levels[action]

def save_model():
    with open(q_table_file, 'wb') as f:
        pickle.dump(q_table, f)
