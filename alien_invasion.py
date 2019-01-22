#导入相关的包
#import sys
import pygame
import matplotlib


#引入相关的类
from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStates
import game_functions as gf
from alien import Alien
from button import Button

#定义函数,游戏的主函数
def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings=Settings()
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    ship=Ship(ai_settings,screen)
    alien=Alien(ai_settings,screen)
    #创建一个用于存储子弹的编组
    bullets=Group()
    aliens=Group()

    #创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)
    #创建用于存储游戏统计信息的实例
    stats=GameStates(ai_settings)

    #创建游戏开始的按钮
    play_button=Button(ai_settings,screen,"Play")

    #游戏主循环
    while True:
        gf.check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,ship,aliens,bullets)
            gf.update_aliens(ai_settings,stats,screen,ship,aliens,bullets)
        #每次循环都重绘屏幕
        gf.update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button)



#运行游戏的主函数
run_game()