class Settings():
    """存储所有的设置类,如飞船的外观、速度等"""
    def __init__(self):
        """初始化游戏的设置"""
        #屏幕的相关设置
        self.screen_width=1200
        self.screen_height=500
        self.bg_color=(230,230,230)
        #子弹设置,宽3像素，高15个像素，深灰色子弹
        self.bullet_speed_factor=1
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=60,60,60
        self.bullets_allowed=3
        #飞船的设置
        self.ship_speed_factor=1.5
        self.ship_limit=3
        #外星人的设置
        self.alien_speed_factor=0.5
        self.alien_drop_speed=10
        #加快游戏节奏的设置
        self.speedup_scale=1.1
        self.initialize_dynamic_settings()
        #1表示向右移动，-1为向左
        self.fleet_direction=1

    #每当玩家开始新游戏时重置速度设置
    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor=1.5
        self.bullet_speed_factor=3
        self.alien_speed_factor=1

        #fleet_direction为1表示向右，为-1表示向左
        self.fleet_direction=1

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor*=self.speedup_scale
        self.bullet_speed_factor*=self.speedup_scale
        self.alien_speed_factor*=self.speedup_scale