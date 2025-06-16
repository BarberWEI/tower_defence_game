from .base_enemy import BaseEnemy

class FastEnemy(BaseEnemy):
    def __init__(self, path, config):
        super().__init__(path, config)
        self.type = 'fast'
        self.health = int(config.enemy_base_health * 0.7)
        self.max_health = self.health
        self.speed = config.enemy_base_speed * 1.5
        self.reward = int(config.enemy_reward * 1.2)
    
    def get_enemy_color(self):
        return (255, 165, 0)  # Orange 