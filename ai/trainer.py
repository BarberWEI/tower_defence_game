import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
import os
from collections import deque
from ai.model import DQN

class DQNTrainer:
    def __init__(self, state_dim, action_dim, model_dir='ai/models/', batch_size=64, gamma=0.99, lr=1e-3, memory_size=10000):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = DQN(state_dim, action_dim).to(self.device)
        self.target_model = DQN(state_dim, action_dim).to(self.device)
        self.target_model.load_state_dict(self.model.state_dict())
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.memory = deque(maxlen=memory_size)
        self.batch_size = batch_size
        self.gamma = gamma
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        self.update_target_steps = 1000
        self.step_count = 0

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state, epsilon=0.1):
        if random.random() < epsilon:
            return random.randint(0, self.model.fc3.out_features - 1)
        state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            q_values = self.model(state)
        return q_values.argmax().item()

    def replay(self):
        if len(self.memory) < self.batch_size:
            return
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        states = torch.FloatTensor(states).to(self.device)
        actions = torch.LongTensor(actions).unsqueeze(1).to(self.device)
        rewards = torch.FloatTensor(rewards).unsqueeze(1).to(self.device)
        next_states = torch.FloatTensor(next_states).to(self.device)
        dones = torch.FloatTensor(dones).unsqueeze(1).to(self.device)

        q_values = self.model(states).gather(1, actions)
        with torch.no_grad():
            next_q_values = self.target_model(next_states).max(1, keepdim=True)[0]
            target = rewards + self.gamma * next_q_values * (1 - dones)
        loss = nn.MSELoss()(q_values, target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.step_count += 1
        if self.step_count % self.update_target_steps == 0:
            self.target_model.load_state_dict(self.model.state_dict())
        if self.step_count % 100 == 0:
            print(f"[DQNTrainer] Step {self.step_count}, Loss: {loss.item():.6f}")

    def save(self, filename):
        torch.save(self.model.state_dict(), os.path.join(self.model_dir, filename))

    def load(self, filename):
        self.model.load_state_dict(torch.load(os.path.join(self.model_dir, filename)))
        self.target_model.load_state_dict(self.model.state_dict()) 