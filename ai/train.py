import numpy as np
from ai.trainer import DQNTrainer
from ai.game import GameAI

STATE_DIM = 10  # Updated to match GameAI.get_state()
ACTION_DIM = 6  # 0-4: place tower, 5: start wave
EPISODES = 1000  # Increased from 500 for better learning
MAX_STEPS = 500
MODEL_SAVE_EVERY = 100  # Save less frequently
SHOW_EVERY = 50  # Show a detailed game every 50 episodes

trainer = DQNTrainer(STATE_DIM, ACTION_DIM, model_dir='ai/models/')

def sample_action(state, epsilon=0.1):
    if np.random.rand() < epsilon:
        return np.random.randint(0, ACTION_DIM)
    else:
        return trainer.act(state)

def action_name(action):
    if action in range(5):
        tower_names = ['Basic', 'Sniper', 'Splash', 'Laser', 'Frost']
        return f"Place {tower_names[action]} Tower"
    elif action == 5:
        return "Start Wave"
    return f"Unknown({action})"

# Track performance metrics
episode_rewards = []
episode_wins = []
episode_lives_lost = []

for episode in range(EPISODES):
    env = GameAI()
    state = env.reset()
    total_reward = 0
    done = False
    steps = 0
    log = []
    waves_started = 0
    initial_lives = env.lives
    
    # Epsilon decay: start at 1.0, decay to 0.05 over all episodes
    epsilon = max(0.05, 1.0 - (episode / EPISODES))
    
    # Debug: Track actions and rewards for all episodes
    episode_actions = []
    episode_rewards = []
    
    # Detailed logging for showcase episodes
    show_detailed = (episode + 1) % SHOW_EVERY == 0
    
    while not done and steps < MAX_STEPS:
        action = sample_action(state, epsilon=epsilon)
        next_state, reward, done, info = env.step(action)
        
        # Track actions and rewards
        episode_actions.append(action)
        episode_rewards.append(reward)
        
        if show_detailed:
            # Detailed logging for showcase episodes
            log.append({
                'step': steps + 1,
                'action': action,
                'action_name': action_name(action),
                'reward': reward,
                'lives': env.lives,
                'money': env.money,
                'wave': env.wave_number,
                'towers': len(env.towers),
                'enemies': len(env.enemies),
                'wave_completed': env.wave_completed,
                'game_over': env.game_over,
                'enemy_positions': [(e.pos, e.path_index, len(e.path)) for e in env.enemies[:3]] if env.enemies else []  # Track first 3 enemies
            })
        
        trainer.remember(state, action, reward, next_state, done)
        trainer.replay()
        state = next_state
        total_reward += reward
        steps += 1
        
        # Count waves started
        if action == 5 and not env.game_over:
            waves_started += 1
    
    # Debug: Store reward before penalties
    reward_before_penalties = total_reward
    
    # Penalize for inactivity or not starting all waves
    penalty = 0
    if waves_started == 0:
        penalty = 0.1  # Penalty for never starting a wave
        total_reward -= penalty
    elif env.wave_number < env.max_waves:
        penalty = 0.1 * (env.max_waves - env.wave_number)  # Penalty for not starting all waves
        total_reward -= penalty
    
    # Track performance metrics
    episode_rewards.append(total_reward)
    lives_lost = initial_lives - env.lives
    episode_lives_lost.append(lives_lost)
    won_game = env.lives > 0 and env.wave_completed and env.wave_number >= env.max_waves
    episode_wins.append(1 if won_game else 0)
    
    # Show detailed gameplay every SHOW_EVERY episodes
    if show_detailed:
        print(f"\n{'='*60}")
        print(f"🎮 EPISODE {episode+1} - DETAILED GAMEPLAY")
        print(f"{'='*60}")
        print(f"Epsilon: {epsilon:.3f} | Final Result: {'🏆 WON' if won_game else '💀 LOST'}")
        print(f"Lives: {initial_lives} → {env.lives} | Money: 100 → {env.money} | Waves: {env.wave_number}/{env.max_waves}")
        print(f"Total Reward: {total_reward:.3f} | Penalty: {penalty:.3f}")
        print("\n📋 ACTION SEQUENCE:")
        
        # Show key actions only (not all 500 steps)
        important_steps = []
        for i, entry in enumerate(log):
            # Show first 10 steps, wave starts, and last 10 steps
            if (i < 10 or 
                entry['action'] == 5 or 
                entry['reward'] > 0.1 or 
                entry['reward'] < -0.1 or
                i >= len(log) - 10):
                important_steps.append(entry)
        
        for entry in important_steps:
            status = ""
            if entry['lives'] < initial_lives:
                status += "💔"
            if entry['wave_completed']:
                status += "✅"
            if entry['game_over']:
                status += "💀"
                
            print(f"  Step {entry['step']:3d}: {entry['action_name']:20} | "
                  f"Reward: {entry['reward']:6.3f} | "
                  f"Lives: {entry['lives']:2d} | Money: ${entry['money']:3d} | "
                  f"Wave: {entry['wave']}/{env.max_waves} | "
                  f"Towers: {entry['towers']:2d} | Enemies: {entry['enemies']:2d} {status}")
        
        if len(log) > len(important_steps):
            print(f"  ... ({len(log) - len(important_steps)} additional steps)")
            
        print(f"\n📊 Episode Summary:")
        print(f"  • Actions: {dict(zip(['Basic','Sniper','Splash','Laser','Frost','Start Wave'], [episode_actions.count(i) for i in range(6)]))}")
        print(f"  • Waves Started: {waves_started}")
        print(f"  • Lives Lost: {lives_lost}")
        print(f"  • Final Status: {'Victory!' if won_game else 'Defeat'}")
        
        # Show learning progress
        if episode >= SHOW_EVERY:
            recent_rewards = episode_rewards[-SHOW_EVERY:]
            recent_wins = sum(episode_wins[-SHOW_EVERY:])
            recent_avg_lives_lost = np.mean(episode_lives_lost[-SHOW_EVERY:])
            
            print(f"\n📈 LEARNING PROGRESS (Last {SHOW_EVERY} episodes):")
            print(f"  • Average Reward: {np.mean(recent_rewards):.3f}")
            print(f"  • Win Rate: {recent_wins}/{SHOW_EVERY} ({100*recent_wins/SHOW_EVERY:.1f}%)")
            print(f"  • Average Lives Lost: {recent_avg_lives_lost:.1f}")
            print(f"  • Best Reward: {max(recent_rewards):.3f}")
    
    # Brief debug output for every episode (not just SHOW_EVERY)
    if not show_detailed:
        print(f"Episode {episode+1:4d}: Reward = {total_reward:6.3f} | "
              f"Lives: {env.lives:2d} | Money: ${env.money:3d} | "
              f"Waves: {waves_started} | Epsilon: {epsilon:.3f}")
    
    # Save model periodically
    if (episode + 1) % MODEL_SAVE_EVERY == 0:
        trainer.save(f'dqn_ep{episode+1}.pth')
        print(f"💾 Model saved at episode {episode+1}")

# Save final model
trainer.save('dqn_final.pth')
print(f"\n🎯 TRAINING COMPLETE!")
print(f"📊 Final Statistics:")
print(f"  • Total Episodes: {EPISODES}")
print(f"  • Overall Win Rate: {sum(episode_wins)}/{EPISODES} ({100*sum(episode_wins)/EPISODES:.1f}%)")
print(f"  • Average Final Reward: {np.mean(episode_rewards):.3f}")
print(f"  • Best Episode Reward: {max(episode_rewards):.3f}")
print(f"💾 Model saved as 'dqn_final.pth'") 