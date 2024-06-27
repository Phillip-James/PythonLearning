import sys
import pygame
from time import sleep
from game_stats import GameStats
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scordboard

class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_width()
        self.settings.screen_height = self.screen.get_height()
        # self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption('Alien Invasion')
        # self.bg.color = (230, 230, 230)
        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self.stats = GameStats(self)
        self.game_active = False

        #创建按钮
        self.play_button = Button(self, "Play")

        # 创建游戏统计实例
        self.stats = GameStats(self)
        self.sb = Scordboard(self)


    def run_game(self):
        """开始游戏主循环"""
        while True:
            # 监听鼠标键盘
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         sys.exit()
            self._check_events()
            if self.game_active:
                self.ship.update()
            # self.bullets.update()
                self._update_bullets()
                self._update_aliens()

            # 删除不要的子弹

            # # self.screen.fill(self.bg_color)
            # self.screen.fill(self.settings.bg_color)
            # self.ship.blitme()
            #
            # # 让最近绘制的屏幕可见
            # pygame.display.flip()
            self._update_screen()
            #每秒60次
            self.clock.tick(60)

    def _check_events(self):
        """ 响应键鼠"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # 向右移动
                    # self.ship.rect.x += 1
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                elif event.key == pygame.K_q:
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    self._fire_bullet()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """点击就送"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #重置信息
            self.settings.initialize_dynamic_seettings()
            self.stats.reset_stats()
            self.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()

            #清空子弹和外星人
            self.bullets.empty()
            self.aliens.empty()

            # 创建外星人舰队, 放置飞船
            self._create_fleet()
            self.ship.center_ship()
            self.sb.prep_ships()

            # hide the mouse
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """创建一个子弹，加入Group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """外星人间距为外星人宽度和高度"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width + 10, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 3 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
             # 添加一行外星人后， 重置x + y
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """创建一个外星人，放在当前行"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # 显示得分
        self.sb.show_score()

        # 判断是否处于活跃状态， 绘制按钮
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_aliens_bullets_collisions()

    def _check_aliens_bullets_collisions(self):
        """..."""
        # 检查碰撞
        collisions = pygame.sprite.groupcollide(self.aliens, self.bullets, True, True)

        if collisions:
            for alien in collisions.values():
                self.stats.score += self.settings.alien_points * len(alien)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()


    def _update_aliens(self):
        """更新外星人"""
        self._check_fleet_edges()
        self.aliens.update()

        #检测外星人和飞船的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1
            self.sb.prep_ships()
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_fleet_edges(self):
        """边缘措施 """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """向下运动，改变方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        # print("change fleet direction")


if __name__ == '__main__':
    # 创建游戏实例并且运行
    ai = AlienInvasion()
    ai.run_game()