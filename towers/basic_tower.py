from .tower import Tower

class BasicTower(Tower):
    """Basic tower with standard stats and targeting"""
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.range = 80
        self.damage = 1
        self.fire_rate = 30  # 2 shots per second at 60 FPS
        self.projectile_speed = 5
        self.size = 12
        self.color = (0, 200, 0)  # Green 