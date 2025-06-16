from .base_enemy import BaseEnemy

class TankEnemy(BaseEnemy):
    def __init__(self, path, config):
        super().__init__(path, config)
        self.type = 'tank'
        self.health = int(config.enemy_base_health * 2.0)
        self.max_health = self.health
        self.speed = config.enemy_base_speed * 0.7
        self.reward = int(config.enemy_reward * 1.5)
    
    def get_enemy_color(self):
        return (128, 0, 128)  # Purple 