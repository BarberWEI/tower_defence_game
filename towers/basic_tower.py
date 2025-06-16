from .base_tower import BaseTower

class BasicTower(BaseTower):
    def __init__(self, pos, config):
        super().__init__(pos, config)
        self.type = 'basic'
        self.range = 150
        self.damage = 20
        self.cooldown = 30
        self.cost = 50
        self.continuous = False
    
    def get_tower_color(self):
        return (100, 100, 100)  # Gray 