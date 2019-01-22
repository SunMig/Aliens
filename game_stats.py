class GameStates():
    """跟踪游戏的统计信息"""
    def __init__(self,ai_settings):
        """初始化统计信息"""
        self.ai_settings=ai_settings;
        self.reset_stats()
        self.game_active=False

    def reset_stats(self):
        self.ships_left=self.ai_settings.ship_limit