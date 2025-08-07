import pygame
from pygame.sprite import Sprite


class Enemy(Sprite):

    # 表示单个敌人的类

    def __init__(self, screen):
        # 初始化敌人并设置其初始位置
        super(Enemy, self).__init__()
        self.screen = screen
        # 加载敌人图像，并设置其rect属性
        self.image = pygame.image.load('picture_file/enemy.bmp')
        self.rect = self.image.get_rect()
        # 每个敌人最初都在荧幕的左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.enemy_speed_factor = 0.5
        self.fleet_drop_speed = 10
        # fleet_direction为1表示向右移，-1表示向左移

        # 存储敌人的准确位置
        self.x = float(self.rect.x)

    def blit_me(self):
        # 在指定位置绘制敌人
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        # 如果敌人处于荧幕边缘，就返回True
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.right <= 0:
            return True

    fleet_direction = 1

    def update(self):
        # 向左或向右移动敌人
        self.x += (self.enemy_speed_factor * self.fleet_direction)
        self.rect.x = self.x
