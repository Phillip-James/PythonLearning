import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """表示外星人"""
    def __init__(self, ai_game):
        """初始化"""
        super().__init__()
        self.screen = ai_game.screen
        #加载外星人图片
        self.image = pygame.image.load('image/alien.bmp')
        self.rect = self.image.get_rect()
        # 初始在左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.settings = ai_game.settings

        #精确位置
        self.x = float(self.rect.x)

    def check_edges(self):
        """边缘 true"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """向右or右移动"""
        # print(self.settings.fleet_direction)
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x