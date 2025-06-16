from ai.game import GameAI

# Test enemy movement
env = GameAI()
env.reset()

print('Testing enemy movement...')
# Start wave 1
success = env.start_next_wave()
print(f'Wave started: {success}, wave={env.wave_number}, enemies={len(env.enemies)}')

# Run for many more steps to see if enemies reach the end
for step in range(200):  # Increased from 30 to 200
    env.update()
    if env.enemies:
        e = env.enemies[0]
        if step % 20 == 0 or e.path_index != prev_path_index if 'prev_path_index' in locals() else True:
            print(f'Step {step:3d}: Enemy pos=({e.pos[0]:.1f},{e.pos[1]:.1f}), path_index={e.path_index}/{len(e.path)-1}, health={e.health}, lives={env.lives}')
        prev_path_index = e.path_index
        
        if e.reached_end():
            print(f'*** ENEMY REACHED END at step {step}! ***')
            break
    else:
        print(f'Step {step:3d}: No enemies, lives={env.lives}')
        if step > 30:  # Only break if we're past initial spawn time
            break
    
    # Check for lives lost
    if env.lives < 20:
        print(f'*** LIVES LOST! Lives: 20 → {env.lives} at step {step} ***')

print(f'Final: enemies={len(env.enemies)}, lives={env.lives}, wave_completed={env.wave_completed}') 