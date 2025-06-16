import numpy as np
from ai.agent import DQNAgent
from ai.game import GameAI

# Example dimensions (update as needed)
STATE_DIM = 10  # Updated to match GameAI.get_state()
ACTION_DIM = 6  # 0-4: place tower, 5: start wave
MODEL_PATH = 'ai/models/dqn_latest.pth'

def main():
    env = GameAI()
    agent = DQNAgent(STATE_DIM, ACTION_DIM, MODEL_PATH)
    state = env.reset()
    done = False
    total_reward = 0
    while not done:
        action = agent.act(state)
        next_state, reward, done, info = env.step(action)
        state = next_state
        total_reward += reward
    print(f"Game finished. Total reward: {total_reward}")

if __name__ == "__main__":
    main() 