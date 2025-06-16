from .base_enemy import BaseEnemy

class BasicEnemy(BaseEnemy):
    def __init__(self, path, config):
        super().__init__(path, config)
        self.type = 'basic'
        self.health = config.enemy_base_health
        self.max_health = self.health
        self.speed = config.enemy_base_speed
        self.reward = config.enemy_reward
    
    def get_enemy_color(self):
        return (255, 0, 0)  # Red 