from pathlib import Path
import sys
import pygame
from blocks import Block
from time import sleep

class Major:
    def __init__(self):
        """初始化"""
        pygame.init()
        # 设置屏幕
        self.screen = pygame.display.set_mode((1500, 700))
        self.bg_color = pygame.Color('White')
        pygame.display.set_caption('Major')
        self.clock = pygame.time.Clock()
        # read txt
        self.index = 0
        self.path = Path('123.rex')
        self.contents = self.path.read_text()
        self.lines = self.contents.split('\n')
        self._title_num = 1

        self.blocks = pygame.sprite.Group()

    def recite_start(self):
        """主循环"""
        while True:
            self._get_events()

            self._update_screen()
            self.clock.tick(30)


    def _get_events(self):
        """响应键盘"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.next_sentence()
                elif event.key == pygame.K_DOWN:
                    self.next_question()
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 检查鼠标的点击答案
                mouse_pos = pygame.mouse.get_pos()
                self._check_abcd(mouse_pos)

    def _check_abcd(self, mouse_pos):
        blocklist = list(self.blocks)
        answer = self._get_answer()
        flag = 0
        for i in range(len(blocklist)):
            if blocklist[i].block.collidepoint(mouse_pos):
                # 检查答案 i + self.title_num
                if len(answer) == 1 and not answer == None:
                    if i - self._title_num + 1 == ord(answer) - 64:
                        blocklist[i].block_color = pygame.Color('Blue')
                        self._create_(self.lines[self.index])
                        self.index += 1
                    else:
                        for block in blocklist:
                            block.block_color = pygame.Color('Red')
                        self._create_(self.lines[self.index])
                        self.index += 1
                    flag = 1
        if flag == 0:
            self.next_question()


    def _get_answer(self):
        # if self.lines[self.index][0] == '答':
        an = self.lines[self.index]
        if not an == '':
            an = an.split('答案：')
            an = list(set(an))
            if '' in an:
                an.remove('')
            return an[0]

    def next_sentence(self):
        """展示下一行"""
        if self.index >= len(self.lines):
            sys.exit()
        elif len(self.blocks) >= 13:
            self.blocks.empty()
            self._title_num = 1
        self._create_(self.lines[self.index])
        self.index += 1

    def next_question(self):
        """下一题"""
        if self.index >= len(self.lines):
            sys.exit()
        if self.lines[self.index] == '':
            self.blocks.empty()
            self._title_num = 1
            self.index += 1
            while not self.lines[self.index][0] == '答':
                self._create_(self.lines[self.index])
                self.index += 1

        else:
            self.next_sentence()

    def _create_(self, msg):
        if msg[0] == '第':
            return
        if len(msg) > 52:
            mid = len(msg) / 2
            mid = int(mid)
            self._create_(msg[:mid])
            self._create_(msg[mid:])
            self._title_num += 1
        else:
            block = Block(len(self.blocks), msg)
            self.blocks.add(block)
        # self.index += 1
    def _update_screen(self):
        """Update images on screen, and flip to the new screen"""
        self.screen.fill(self.bg_color)
        for block in self.blocks.sprites():
            block.draw(self.screen)

        pygame.display.flip()

if __name__ == '__main__':
    ai = Major()
    ai.recite_start()

# path = Path('123.rex')
# contents = path.read_text()
# lines = contents.split('\n')
# flag = True
# index = 0
# while index < len(lines):
#     while len(lines[index]) > 5:
#         print(lines[index])
#         index += 1
#     if lines[index] != '':
#         sleep(7)
#     else:
#         sleep(3)
#     print(lines[index])
#     index += 1
