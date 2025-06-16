import numpy as np
import torch
from ai.trainer import DQNTrainer
from ai.game import GameAI

STATE_DIM = 12  # Expanded state for better decision making
ACTION_DIM = 6  # 0-4: place tower, 5: start wave
EPISODES = 2000  # Increased for better learning
MAX_STEPS = 300  # Reduced since path is shorter now
MODEL_SAVE_EVERY = 200  # Save less frequently
SHOW_EVERY = 100  # Show detailed game every 100 episodes

trainer = DQNTrainer(STATE_DIM, ACTION_DIM, model_dir='ai/models/')

def get_valid_actions(env):
    """Return list of valid actions to prevent invalid moves"""
    valid_actions = []
    
    # Always allow tower placement attempts (let the game handle invalid placements)
    valid_actions.extend([0, 1, 2, 3, 4])  # All tower types
    
    # Check if we can start wave
    if env.wave_completed and env.wave_number < env.max_waves:
        valid_actions.append(5)
    
    return valid_actions

def sample_action(state, epsilon, env):
    """Improved action sampling with validity checking"""
    valid_actions = get_valid_actions(env)
    
    if np.random.rand() < epsilon:
        # Random action from valid actions only
        return np.random.choice(valid_actions)
    else:
        # Convert numpy array to tensor if needed
        if isinstance(state, np.ndarray):
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
        else:
            state_tensor = state.unsqueeze(0)
            
        # Get Q-values for all actions
        q_values = trainer.model(state_tensor).cpu().data.numpy()[0]
        
        # Mask invalid actions with very low values
        masked_q_values = np.full(ACTION_DIM, -1000.0)
        for action in valid_actions:
            masked_q_values[action] = q_values[action]
        
        return np.argmax(masked_q_values)

def action_name(action):
    if action in range(5):
        tower_names = ['Basic', 'Sniper', 'Splash', 'Laser', 'Frost']
        return f"Place {tower_names[action]} Tower"
    elif action == 5:
        return "Start Wave"
    return f"Unknown({action})"

def calculate_strategic_reward(env, action, prev_state, success):
    """Calculate strategic rewards based on game state and action effectiveness"""
    reward = 0
    
    if action in range(5):  # Tower placement
        if success:
            # Reward early tower placement more generously
            if env.wave_number == 0:
                reward += 0.5  # Bigger bonus for preparation
            else:
                reward += 0.2  # Good bonus during combat
            
            # Bonus for tower diversity
            tower_types = set(getattr(t, 'type', 'basic') for t in env.towers)
            if len(tower_types) > 1:
                reward += 0.2  # Better diversity bonus
        else:
            # Much smaller penalty for failed tower placement
            reward -= 0.1  # Small penalty, not punitive
    
    elif action == 5:  # Start wave
        if success:
            # Good reward for starting waves
            reward += 0.3
            # Bonus for having towers before starting
            if len(env.towers) > 0:
                reward += 0.1 * min(len(env.towers), 5)  # Cap bonus to prevent exploitation
        else:
            # Small penalty for invalid wave starts
            reward -= 0.1  # Much smaller penalty
    
    return reward

# Track performance metrics
episode_rewards = []
episode_wins = []
episode_lives_lost = []
episode_towers_built = []

print("🚀 Starting Enhanced Tower Defense Training!")
print(f"Episodes: {EPISODES}, Max Steps: {MAX_STEPS}")
print("Improvements: Action filtering, strategic rewards, better exploration")

for episode in range(EPISODES):
    env = GameAI()
    state = env.reset()
    total_reward = 0
    done = False
    steps = 0
    log = []
    waves_started = 0
    initial_lives = env.lives
    towers_built = 0
    
    # More gradual epsilon decay: start at 0.95, decay to 0.1 over all episodes
    epsilon = max(0.1, 0.95 - (episode / EPISODES) * 0.85)
    
    # Track actions and rewards for all episodes
    episode_actions = []
    episode_step_rewards = []
    
    # Detailed logging for showcase episodes
    show_detailed = (episode + 1) % SHOW_EVERY == 0
    
    while not done and steps < MAX_STEPS:
        prev_state = env.get_state()
        action = sample_action(state, epsilon, env)
        next_state, base_reward, done, info = env.step(action)
        
        # Calculate strategic reward
        action_success = base_reward > 0 or (action == 5 and env.wave_number > prev_state[2] * env.max_waves)
        strategic_reward = calculate_strategic_reward(env, action, prev_state, action_success)
        
        # Combine rewards
        total_step_reward = base_reward + strategic_reward
        
        # Track successful tower builds
        if action in range(5) and len(env.towers) > towers_built:
            towers_built = len(env.towers)
        
        # Track actions and rewards
        episode_actions.append(action)
        episode_step_rewards.append(total_step_reward)
        
        if show_detailed:
            # Detailed logging for showcase episodes
            log.append({
                'step': steps + 1,
                'action': action,
                'action_name': action_name(action),
                'base_reward': base_reward,
                'strategic_reward': strategic_reward,
                'total_reward': total_step_reward,
                'lives': env.lives,
                'money': env.money,
                'wave': env.wave_number,
                'towers': len(env.towers),
                'enemies': len(env.enemies),
                'wave_completed': env.wave_completed,
                'game_over': env.game_over,
                'valid_actions': get_valid_actions(env)
            })
        
        trainer.remember(state, action, total_step_reward, next_state, done)
        trainer.replay()
        state = next_state
        total_reward += total_step_reward
        steps += 1
        
        # Count waves started
        if action == 5 and not env.game_over:
            waves_started += 1
    
    # Final reward adjustments - much more balanced
    reward_before_penalties = total_reward
    
    # Completion bonuses (positive reinforcement focus)
    if env.wave_completed and env.wave_number >= env.max_waves:
        # Big bonus for completing the game
        completion_bonus = 5.0
        total_reward += completion_bonus
        
        # Efficiency bonus for completing quickly
        efficiency_bonus = max(0, (MAX_STEPS - steps) / MAX_STEPS) * 2.0
        total_reward += efficiency_bonus
    elif env.wave_number > 0:
        # Partial completion bonus
        progress_bonus = 1.0 * env.wave_number / env.max_waves
        total_reward += progress_bonus
    
    # Tower building bonus
    if towers_built > 0:
        total_reward += 0.2 * towers_built
    
    # Lives preservation bonus
    lives_bonus = 0.2 * env.lives
    total_reward += lives_bonus
    
    # Base survival bonus (positive baseline)
    survival_bonus = 2.0  # Everyone gets this for trying
    total_reward += survival_bonus
    
    # Small penalty only for completely inactive play
    if waves_started == 0 and towers_built == 0:
        total_reward -= 1.0  # Small penalty for doing nothing
    
    # Track performance metrics
    episode_rewards.append(total_reward)
    lives_lost = initial_lives - env.lives
    episode_lives_lost.append(lives_lost)
    episode_towers_built.append(towers_built)
    won_game = env.lives > 0 and env.wave_completed and env.wave_number >= env.max_waves
    episode_wins.append(1 if won_game else 0)
    
    # Show detailed gameplay every SHOW_EVERY episodes
    if show_detailed:
        print(f"\n{'='*70}")
        print(f"🎮 EPISODE {episode+1} - ENHANCED TRAINING ANALYSIS")
        print(f"{'='*70}")
        print(f"Epsilon: {epsilon:.3f} | Result: {'🏆 VICTORY' if won_game else '💀 DEFEAT'}")
        print(f"Lives: {initial_lives} → {env.lives} | Money: 100 → {env.money} | Waves: {env.wave_number}/{env.max_waves}")
        print(f"Towers Built: {towers_built} | Total Reward: {total_reward:.3f}")
        print("\n📋 KEY STRATEGIC ACTIONS:")
        
        # Show only strategically important actions
        important_actions = []
        for i, entry in enumerate(log):
            # Show successful actions, major rewards/penalties, and critical moments
            if (abs(entry['total_reward']) > 0.15 or 
                entry['action'] == 5 and len([x for x in log[:i] if x['action'] == 5]) < 3 or  # First few wave attempts
                entry['lives'] < initial_lives or
                entry['towers'] > (log[i-1]['towers'] if i > 0 else 0)):  # Tower built
                important_actions.append(entry)
        
        for entry in important_actions[:15]:  # Limit to 15 most important actions
            status = ""
            if entry['lives'] < initial_lives:
                status += "💔"
            if entry['towers'] > 0:
                status += "🏗️"
            if entry['wave_completed']:
                status += "✅"
            if entry['total_reward'] > 0.3:
                status += "⭐"
                
            print(f"  Step {entry['step']:3d}: {entry['action_name']:20} | "
                  f"Reward: {entry['total_reward']:6.3f} ({entry['base_reward']:+.2f}+{entry['strategic_reward']:+.2f}) | "
                  f"Lives: {entry['lives']:2d} | Money: ${entry['money']:3d} | "
                  f"Towers: {entry['towers']:2d} | Valid: {len(entry['valid_actions'])} {status}")
            
        print(f"\n📊 STRATEGIC ANALYSIS:")
        action_counts = [episode_actions.count(i) for i in range(6)]
        action_efficiency = [action_counts[i] / max(1, sum(1 for j, r in enumerate(episode_step_rewards) if episode_actions[j] == i and r > 0)) for i in range(6)]
        
        print(f"  • Action Counts: {dict(zip(['Basic','Sniper','Splash','Laser','Frost','Start Wave'], action_counts))}")
        print(f"  • Towers Built: {towers_built} (Success Rate: {towers_built/max(1, sum(action_counts[:5]))*100:.1f}%)")
        print(f"  • Wave Efficiency: {waves_started} attempts for {env.wave_number} waves")
        print(f"  • Lives Preserved: {env.lives}/{initial_lives} ({env.lives/initial_lives*100:.1f}%)")
        print(f"  • Final Status: {'Complete Victory!' if won_game else f'Defeated (Wave {env.wave_number}/{env.max_waves})'}")
        
        # Show learning progress
        if episode >= SHOW_EVERY:
            recent_rewards = episode_rewards[-SHOW_EVERY:]
            recent_wins = sum(episode_wins[-SHOW_EVERY:])
            recent_avg_lives_lost = np.mean(episode_lives_lost[-SHOW_EVERY:])
            recent_avg_towers = np.mean(episode_towers_built[-SHOW_EVERY:])
            
            print(f"\n📈 LEARNING PROGRESS (Last {SHOW_EVERY} episodes):")
            print(f"  • Average Reward: {np.mean(recent_rewards):.3f}")
            print(f"  • Win Rate: {recent_wins}/{SHOW_EVERY} ({100*recent_wins/SHOW_EVERY:.1f}%)")
            print(f"  • Average Lives Lost: {recent_avg_lives_lost:.1f}")
            print(f"  • Average Towers Built: {recent_avg_towers:.1f}")
            print(f"  • Best Reward: {max(recent_rewards):.3f}")
            if episode >= 2 * SHOW_EVERY:
                prev_rewards = episode_rewards[-2*SHOW_EVERY:-SHOW_EVERY]
                improvement = np.mean(recent_rewards) - np.mean(prev_rewards)
                print(f"  • Improvement: {improvement:+.3f} {'📈' if improvement > 0 else '📉'}")
    
    # Brief output for every episode
    if not show_detailed:
        status = "🏆" if won_game else "💀"
        print(f"Episode {episode+1:4d}: {status} Reward={total_reward:6.3f} | "
              f"Lives:{env.lives:2d} | Towers:{towers_built:2d} | "
              f"Waves:{env.wave_number}/{env.max_waves} | ε:{epsilon:.3f}")
    
    # Save model periodically
    if (episode + 1) % MODEL_SAVE_EVERY == 0:
        trainer.save(f'dqn_enhanced_ep{episode+1}.pth')
        recent_win_rate = sum(episode_wins[-100:]) / min(100, len(episode_wins)) * 100
        print(f"💾 Model saved at episode {episode+1} (Win rate: {recent_win_rate:.1f}%)")

# Save final model
trainer.save('dqn_enhanced_final.pth')
print(f"\n🎯 ENHANCED TRAINING COMPLETE!")
print(f"📊 Final Statistics:")
print(f"  • Total Episodes: {EPISODES}")
print(f"  • Overall Win Rate: {sum(episode_wins)}/{EPISODES} ({100*sum(episode_wins)/EPISODES:.1f}%)")
print(f"  • Average Final Reward: {np.mean(episode_rewards):.3f}")
print(f"  • Best Episode Reward: {max(episode_rewards):.3f}")
print(f"  • Average Towers Built: {np.mean(episode_towers_built):.1f}")
print(f"  • Average Lives Preserved: {20 - np.mean(episode_lives_lost):.1f}/20")
print(f"💾 Enhanced model saved as 'dqn_enhanced_final.pth'") 