class Settings:
    """储存游戏中所有设置的类"""
    def __init__(self):
        """初始化游戏设置"""
        #屏幕
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_limit = 3
        self.bullet_color = (60, 60, 60)
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullets_allowed = 20
        self.fleet_drop_speed = 100

        #以什么样的速度加快
        self.speedup_scale = 1.1
        self.initialize_dynamic_seettings()
        self.score_scale = 1.5

    def initialize_dynamic_seettings(self):
        """初始化"""
        self.ship_speed = 6
        self.bullet_speed = 2.6
        self.alien_speed = 1.0
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        """提高速度"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)