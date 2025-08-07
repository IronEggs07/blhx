import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, screen):
        super(Ship, self).__init__()
        # 初始化舰船并设置其初始位置
        ship_speed_factor = 1.5
        self.screen = screen
        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('picture_file/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.ship_speed_factor = ship_speed_factor
        # 将每艘新船放在萤幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        self.bottom = self.rect.bottom
        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        # 设置移动速度

    def update(self):
        # 根据移动标志调整飞船的位置
        # 更新舰船的center值，而不是rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ship_speed_factor
        if self.moving_left and self.rect.right > 32:
            self.centerx -= self.ship_speed_factor
        if self.moving_up and self.rect.bottom > 40:
            self.centery -= self.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ship_speed_factor

        # 根据self.center更新rect对象
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def blit_me(self):
        # 在指定位置绘制舰船
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        # 让舰船归位
        self.center = self.screen_rect.centerx, self.screen_rect.bottom
