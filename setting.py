class GAME:
    # 存储《Azurlane》中所有设置相关的类
    def __init__(self):
        # 初始化游戏的设置
        # 荧幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # 子弹设置
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        # 飞船设置
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        # 敌人设置
        self.enemy_speed_factor = 1
        self.fleet_drop_speed = 10
        # fleet_direction为1表示向右移，-1表示向左移
        fleet_direction = 1

