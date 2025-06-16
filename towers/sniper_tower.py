from .base_tower import BaseTower

class SniperTower(BaseTower):
    def __init__(self, pos, config):
        super().__init__(pos, config)
        self.type = 'sniper'
        self.range = 300
        self.damage = 50
        self.cooldown = 60
        self.cost = 100
        self.continuous = False
    
    def get_tower_color(self):
        return (0, 0, 255)  # Blue 