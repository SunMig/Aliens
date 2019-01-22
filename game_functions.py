import sys
import pygame

from Bullet import Bullet
from alien import Alien
from time import sleep
#存放所有的事件函数
def check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets):
    """响应按键和鼠标的事件，检查按键按下或者松开"""
    # 监视鼠标事件和键盘
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type==pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()#获取鼠标点击的位置
            check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    """在玩家单击play按钮时开始新游戏"""
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #隐藏光标/游戏开始后隐藏
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active=True
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建新的外星人和飞船
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship();

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    """响应按键按下的函数"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key==pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key==pygame.K_q:
        sys.exit()

def check_keyup_events(event,ship):
    """响应松开的函数"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button):
    """更新屏幕上的图像"""
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()#绘制的方法
    aliens.draw(screen)
    #如果游戏处于非活动状态就创建play按钮
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

def update_bullets(ai_settings,screen,ship,aliens,bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens)==0:
        #删除现有子弹并新建一群外星人
        bullets.empty();
        #加快新的外星人速度
        ai_settings.increase_speed()
        create_fleet(ai_settings,screen,ship,aliens);


def fire_bullet(ai_settings,screen,ship,bullets):
    # 创建一个子弹，并将其放入编组中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

#一行能有几个外星人
def get_number_aliens_x(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x

def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y=(ai_settings.screen_width-(3*alien_height)-ship_height)
    number_rows=int(available_space_y/(6*alien_height))
    return number_rows


#创建多个外星人
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    alien=Alien(ai_settings,screen)
    alien_width=alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number

    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

#创建一行外星人
def create_fleet(ai_settings,screen,ship,aliens):
    alien=Alien(ai_settings,screen)
    number_alien_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

    #循环实现，把创建的外星人放进空的编组中
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
    """响应被外星人撞到的飞船"""
    #将ships_left减1
    if stats.ships_left>0:
        #清空外星人列表和子弹列表
        stats.ships_left-=1
        aliens.empty()
        bullets.empty()
        #创建新外星人
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        #暂停
        sleep(0.5)
    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)

#更新外星人的位置
def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
    #调用方法检查每一个外星人是否到了屏幕边缘
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    #检测外星人与飞船之间的碰撞，碰到之后游戏结束
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets)

    #检查是否有外星人到达屏幕的底部
    check_aliens_buttom(ai_settings,stats,screen,ship,aliens,bullets)

def check_aliens_buttom(ai_settings,stats,screen,ship,aliens,bullets):
    """检查外星人是否到达了屏幕底部"""
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            #重新开始游戏
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
            break


#检查是否位于屏幕边缘
def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

#将外星人下移同时将方向值改变
def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.alien_drop_speed
    ai_settings.fleet_direction*=-1
