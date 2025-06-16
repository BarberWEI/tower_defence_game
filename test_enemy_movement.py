from ai.game import GameAI

# Test enemy movement and path completion
env = GameAI()
env.reset()

print('=== COMPREHENSIVE ENEMY MOVEMENT TEST ===')
print(f'Path points: {env.path.points}')
print(f'Path length: {len(env.path.points)} points')

# Calculate total path distance
total_distance = 0
for i in range(len(env.path.points) - 1):
    p1, p2 = env.path.points[i], env.path.points[i + 1]
    dist = ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**0.5
    total_distance += dist
    print(f'  Segment {i}: {p1} -> {p2}, distance: {dist:.1f}')

print(f'Total path distance: {total_distance:.1f} pixels')

# Start wave 1
success = env.start_next_wave()
print(f'\nWave started: {success}, wave={env.wave_number}, enemies={len(env.enemies)}')

# Call update to actually spawn enemies
env.update()
print(f'After first update: enemies={len(env.enemies)}')

# Debug WaveManager state
wm = env.wave_manager
print(f'WaveManager state:')
print(f'  wave_in_progress: {wm.wave_in_progress}')
print(f'  enemies_spawned: {wm.enemies_spawned}')
print(f'  total_enemies: {wm.total_enemies}')
print(f'  spawn_timer: {wm.spawn_timer}')
print(f'  spawn_delay: {wm.spawn_delay}')

# Manually test WaveManager update
print(f'\nTesting WaveManager.update() directly:')
for i in range(5):
    new_enemies = wm.update()
    print(f'  Update {i}: spawned {len(new_enemies)} enemies, timer={wm.spawn_timer}, total_spawned={wm.enemies_spawned}')
    if new_enemies:
        print(f'    Enemy type: {type(new_enemies[0]).__name__}')
        break

if not env.enemies and not new_enemies:
    print("ERROR: Still no enemies spawned after manual testing!")
    print("Checking enemy class imports...")
    from enemies import BasicEnemy, FastEnemy
    print(f"BasicEnemy: {BasicEnemy}")
    print(f"FastEnemy: {FastEnemy}")
    
    # Try creating enemy manually
    try:
        manual_enemy = BasicEnemy(env.path.points, env.config)
        print(f"Manual enemy creation successful: {manual_enemy}")
        print(f"  Speed: {manual_enemy.speed}")
        print(f"  Health: {manual_enemy.health}")
    except Exception as e:
        print(f"Manual enemy creation failed: {e}")
    
    exit()

# Continue with original test if enemies spawn
enemy = env.enemies[0] if env.enemies else new_enemies[0]
print(f'Enemy speed: {enemy.speed} pixels/frame')
print(f'Estimated time to complete: {total_distance / enemy.speed:.1f} frames')

# Track enemy progress
initial_lives = env.lives
prev_path_index = -1
prev_enemies = []

for step in range(300):  # Reduced since path is shorter
    env.update()
    
    if env.enemies:
        e = env.enemies[0]
        if step % 25 == 0 or e.path_index != prev_path_index:
            print(f'Step {step:3d}: pos=({e.pos[0]:.1f},{e.pos[1]:.1f}), path_index={e.path_index}/{len(e.path)-1}, health={e.health}, lives={env.lives}')
            prev_path_index = e.path_index
        
        # Check if enemy reached end
        if e.reached_end():
            print(f'*** ENEMY REACHED END at step {step}! ***')
            print(f'Lives before: {initial_lives}, Lives after: {env.lives}')
            break
            
        # Check if enemy was removed
        if len(env.enemies) < len(prev_enemies):
            print(f'*** ENEMY REMOVED at step {step}! ***')
            print(f'Lives: {initial_lives} -> {env.lives}')
            if env.lives < initial_lives:
                print('Lives lost - enemy reached end!')
            else:
                print('Enemy killed by tower!')
            break
            
        prev_enemies = env.enemies[:]
    else:
        print(f'Step {step:3d}: No enemies remaining, lives={env.lives}')
        if env.lives < initial_lives:
            print(f'Lives lost: {initial_lives} -> {env.lives}')
        break
    
    # Check for lives lost
    if env.lives < initial_lives:
        print(f'*** LIVES LOST! {initial_lives} -> {env.lives} at step {step} ***')

print(f'\nFinal: enemies={len(env.enemies)}, lives={env.lives}, wave_completed={env.wave_completed}')
print(f'Lives lost: {initial_lives - env.lives}') 