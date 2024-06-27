class GameStats:
    """跟踪游戏信息"""

    def __init__(self, ai_game):
        """初始化"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = 0
        self.level = 1

    def reset_stats(self):
        """初始化游戏运行时间可能变化的量"""
        self.ship_left = self.settings.ship_limit
        self.score = 0
