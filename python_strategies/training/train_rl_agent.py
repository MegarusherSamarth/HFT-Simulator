# Trains a Deep Q-Learning (DQN) agent on historical tick data.
# The agent learns to BUY / SELL / HOLD based on price + volume state.

import random
import numpy as np
import pandas as pd
from collections import deque
from pathlib import Path
import torch
import torch.nn as nn
import torch.optim as optim

# Q-Network
class QNetwork(nn.Module):
    def __init__(self, input_dim=2, hidden_dim=64, output_dim=3):
        # input_dim: price, volume
        # output_dim: BUY, SELL, HOLD
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )
    
    def forward(self, x):
        return self.net(x)
    
# Replay Buffer
class ReplayBuffer:
    def __init__(self, capacity=50000):
        self.buffer = deque(maxlen=capacity)
        
    def push(self, state, action, reward, next_state):
        self.buffer.append((state, action, reward, next_state))
        
    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states = zip(*batch)
        return (
            torch.tensor(states, dtype=torch.float32),
            torch.tensor(actions, dtype=torch.long),
            torch.tensor(rewards, dtype=torch.float32),
            torch.tensor(next_states, dtype=torch.float32)
        )
    
    def __len__(self):
        return len(self.buffer)
    
# RL Trainer
class RLTrainer:
    def __init__(self):
        self.gamma = 0.99
        self.lr = 0.001
        self.batch_size = 64
        self.epsilon = 1.0
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.995
        self.model = QNetwork()
        self.target_model = QNetwork()
        self.target_model.load_state_dict(self.model.state_dict())
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.loss_fn = nn.MSELoss()
        self.buffer = ReplayBuffer()
        self.model_path = Path(__file__).resolve().parent.parent / "models" / "rl_agent.pt"
    
    def choose_action(self, state):
        # Epsilon-greedy action selection.
        if random.random() < self.epsilon:
            return random.randint(0, 2)  # BUY, SELL, HOLD
        with torch.no_grad():
            q_values = self.model(torch.tensor(state, dtype=torch.float32))
            return torch.argmax(q_values).item()
    
    def compute_reward(self, current_price, next_price, action):
        # Reward based on price movement.
        if action == 0: # BUY
            return next_price - current_price
        elif action == 1: # SELL
            return current_price - next_price
        else: # HOLD
            return 0.0
    
    def train_step(self):
        if len(self.buffer) < self.batch_size:
            return
        
        states, actions, rewards, next_states = self.buffer.sample(self.batch_size)
        
        q_values = self.model(states)
        next_q_values = self.target_model(next_states)
        
        q_target = q_values.clone()
        for i in range(self.batch_size):
            q_target[i, actions[i]] = rewards[i] + self.gamma * torch.max(next_q_values[i])
        
        loss = self.loss_fn(q_values, q_target.detach())
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
    
    def update_target_network(self):
        self.target_model.load_state_dict(self.model.state_dict())
    
    def train(self, df):
        prices = df["price"].values
        volumes = df["volume"].values
        print ("[INFO] Starting RL agent training... ")
        
        for i in range(len(df) - 1):
            state = np.array([prices[i], volumes[i]], dtype=np.float32)
            next_state = np.array([prices[i+1], volumes[i+1]], dtype=np.float32)
            action = self.choose_action(state)
            reward = self.compute_reward(prices[i], prices[i+1], action)
            
            self.buffer.push(state, action, reward, next_state)
            self.train_step()
            
            # Update taget network periodically
            if i % 200 == 0:
                self.update_target_network()
                
            # Epsilon decay
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay
        
        torch.save(self.model.state_dict(), self.model_path)
        print(f"[INFO] RL agent saved to {self.model_path}")

# Main
if __name__ == "__main__":
    data_path = Path(__file__).resolve().parents[2] / "data_feed" / "raw_Data" / "btc_usdt.csv"
    df = pd.read_csv(data_path)
    
    trainer = RLTrainer()
    trainer.train(df)