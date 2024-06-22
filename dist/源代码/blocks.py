import pygame

class Block(pygame.sprite.Sprite):
    """文本框的类"""

    def __init__(self, num, msg):
        super().__init__()
        # 设置字体
        self.font = pygame.font.SysFont('SimHei', 28)
        self.text_color = pygame.Color('Black')
        #一个文本框参数
        self.width = 1200
        self.height = 30
        self.block_color = pygame.Color('Green')
        self.creat_a_block(msg, num)

    def creat_a_block(self, msg, num):
        """创建文本框，并且写字"""
        self.block = pygame.Rect(0, 0, self.width, self.height)
        self.set_rect(num)
        self.msg_image = self.font.render(msg, True, self.text_color, self.block_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.block.center

    def set_rect(self, num):
        """设置位置"""
        self.block.y = num * (self.height + 10)
        self.block.x = 100

    def draw(self, screen):
        """"""
        screen.fill(self.block_color, self.block)
        screen.blit(self.msg_image, self.msg_image_rect)
        # pygame.draw.rect(screen, self.block_color, self.block)