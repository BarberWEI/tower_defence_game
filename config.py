class GameConfig:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        
        # Starting resources
        self.starting_money = int(100 + difficulty * 50)  # 100-150 money
        self.starting_lives = 20  # Fixed number of lives
        
        # Enemy base stats
        self.enemy_base_health = 100
        self.enemy_base_speed = 2
        self.enemy_reward = 10
        
        # Tower base stats
        self.tower_base_range = 150
        self.tower_base_damage = 20
        self.tower_base_cooldown = 1000  # milliseconds
        
        # Tower costs
        self.tower_costs = {
            'basic': 50,
            'sniper': 100,
            'splash': 150,
            'laser': 200
        }
        
        # Tower unlock difficulties
        self.tower_unlock_difficulties = {
            'basic': 0.0,
            'sniper': 0.3,
            'splash': 0.5,
            'laser': 0.7
        }
    
    def get_tower_cost(self, tower_type):
        return self.tower_costs.get(tower_type, 100)
    
    def get_tower_unlock_difficulty(self, tower_type):
        return self.tower_unlock_difficulties.get(tower_type, 1.0)
    
    def is_tower_available(self, tower_type):
        return self.difficulty >= self.get_tower_unlock_difficulty(tower_type)
    
    def setup_difficulty_settings(self):
        # Starting resources
        self.starting_money = int(100 + (1 - self.difficulty) * 200)  # More money for lower difficulty
        self.starting_lives = int(20 + (1 - self.difficulty) * 10)    # More lives for lower difficulty
        
        # Enemy settings
        self.enemy_base_health = int(100 + self.difficulty * 200)     # More health for higher difficulty
        self.enemy_base_speed = 2 + self.difficulty * 1.5             # Faster for higher difficulty
        self.enemy_reward = int(10 + (1 - self.difficulty) * 15)      # More reward for lower difficulty
        
        # Wave settings
        self.enemies_per_wave = int(5 + self.difficulty * 5)          # More enemies for higher difficulty
        self.wave_delay = max(30, int(60 - self.difficulty * 30))     # Shorter delay for higher difficulty
        
        # Tower settings
        self.available_towers = self.get_available_towers()
    
    def get_available_towers(self):
        # Basic tower always available
        towers = {
            'basic': {
                'cost': 50,
                'damage': 20,
                'range': 150,
                'cooldown': 30
            }
        }
        
        # Add more tower types based on difficulty
        if self.difficulty >= 0.3:
            towers['sniper'] = {
                'cost': 100,
                'damage': 50,
                'range': 300,
                'cooldown': 60
            }
        
        if self.difficulty >= 0.5:
            towers['splash'] = {
                'cost': 150,
                'damage': 15,
                'range': 100,
                'cooldown': 45,
                'splash_radius': 50
            }
        
        if self.difficulty >= 0.7:
            towers['laser'] = {
                'cost': 200,
                'damage': 10,
                'range': 200,
                'cooldown': 5,
                'continuous': True
            }
        
        return towers
    
    def get_starting_positions(self):
        # Define possible starting positions based on difficulty
        positions = {
            'easy': [(0, 300)],                    # Middle left
            'medium': [(0, 150), (0, 450)],        # Top and bottom left
            'hard': [(0, 100), (0, 300), (0, 500)] # Three starting points
        }
        
        # Select starting positions based on difficulty
        if self.difficulty < 0.3:
            return positions['easy']
        elif self.difficulty < 0.7:
            return positions['medium']
        else:
            return positions['hard']
    
    def get_enemy_types(self):
        # Define enemy types based on difficulty
        types = {
            'basic': {
                'health_multiplier': 1.0,
                'speed_multiplier': 1.0,
                'reward_multiplier': 1.0
            }
        }
        
        if self.difficulty >= 0.3:
            types['fast'] = {
                'health_multiplier': 0.7,
                'speed_multiplier': 1.5,
                'reward_multiplier': 1.2
            }
        
        if self.difficulty >= 0.5:
            types['tank'] = {
                'health_multiplier': 2.0,
                'speed_multiplier': 0.7,
                'reward_multiplier': 1.5
            }
        
        if self.difficulty >= 0.7:
            types['boss'] = {
                'health_multiplier': 3.0,
                'speed_multiplier': 0.5,
                'reward_multiplier': 2.0
            }
        
        return types 