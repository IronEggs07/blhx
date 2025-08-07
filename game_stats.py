class GameStats:

    # 跟踪游戏的统计信息
    def __init__(self):
        self.ships_left = None
        self.reset_stats()
        # 游戏一开始处于非激活状态
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        self.ships_left = 2
        self.score = 0
        self.level = 1








