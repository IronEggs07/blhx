import pygame
from ship import Ship
from enemy import Enemy
import game_functions
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    # 初始化pygame、设置和荧幕对象
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Azurlane")
    # 创建play按钮
    play_button = Button(screen, "play")
    # 设置背景色
    bg_color = (0, 0, 255)

    # 创建一艘舰船
    ship = Ship(screen)
    # 创建游戏统计信息
    stats = GameStats()
    # 创建计分板
    sb = Scoreboard(screen, stats)
    # 创建一个敌人
    enemy = Enemy(screen)
    # 创建一个用于存储子弹和敌人的编组
    bullets = Group()
    enemies = Group()
    # 创建敌人群
    game_functions.create_fleet(screen, ship, enemies)
    # 开始游戏的主循环
    while True:
        # 监视键盘和鼠标事件
        game_functions.check_event(screen, stats, sb, play_button, ship, enemies, bullets)
        if stats.game_active:
            ship.update()
            game_functions.update_bullet(screen, stats, sb, ship, enemies, bullets)
            game_functions.update_enemies(screen, stats, sb, ship, enemies, bullets)

        game_functions.update_screen(bg_color, screen, stats, sb, ship, enemies, bullets, play_button)
        # print(len(bullets))
        # print(len(enemies))


run_game()
