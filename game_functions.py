import sys
import pygame
from bullet import Bullet
from enemy import Enemy
from time import sleep
fleet_drop_speed = 10


# 移动键盘右左上下
# 响应按键
def check_keydown_event(event, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


# 响应松开按键
def check_keyup_event(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


# 响应键盘和鼠标事件
def check_event(screen, stats, sb, play_button, ship, enemies, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(screen, stats, sb, play_button, ship, enemies, bullets, mouse_x, mouse_y)


# 在玩家点击play时开始游戏
def check_play_button(screen, stats, sb, play_button, ship, enemies, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ship()
        enemies.empty()
        bullets.empty()
        pygame.mouse.set_visible(False)
        create_fleet(screen, ship, enemies)
        ship.center_ship()


# 更新子弹的位置，删除已消失的子弹
def update_bullet(screen, stats, sb, ship, enemies, bullets):
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_enemy_collisions(screen, stats, sb, ship, enemies, bullets)

    # 更新子弹的位置
    bullets.update()


# 创建一颗子弹，并将其加入到编组bullets中
def fire_bullet(screen, ship, bullets):
    new_bullet = Bullet(screen, ship)
    print("aaa")
    bullets.add(new_bullet)


# 计算每行可容纳多少个敌人
def get_number_enemies_x(enemy_width):
    # 敌人的间距和敌人的宽度
    available_space_x = 1200 - 2 * enemy_width
    number_enemies_x = int(available_space_x / (2 * enemy_width))
    return number_enemies_x


# 计算荧幕可以容纳多少行敌人
def get_number_rows(ship_height, enemy_height):
    available_space_y = 800 - (3 * enemy_height) - (8 * ship_height)
    number_rows = int(available_space_y / (2 * enemy_height))
    return number_rows


# 创建第一个敌人并让其加入当前行
def create_enemy(screen, enemies, enemy_number, row_number):
    enemy = Enemy(screen)
    enemy_width = enemy.rect.width
    enemy.x = enemy_width + 2 * enemy_width * enemy_number
    enemy.rect.x = enemy.x
    enemy.rect.y = enemy.rect.height + 2 * enemy.rect.height * row_number
    enemies.add(enemy)


# 创建敌人群
def create_fleet(screen, ship, enemies):
    enemy = Enemy(screen)
    enemy_width = enemy.rect.width
    # enemy_height = enemy.rect.height
    number_enemies_x = get_number_enemies_x(enemy.rect.width)
    number_rows = get_number_rows(ship.rect.height, enemy.rect.height)
    # 创建第一行敌人
    for row_number in range(number_rows):
        for enemy_number in range(number_enemies_x):
            create_enemy(screen, enemies, enemy_number, row_number)


# 更新荧幕上的图像，并切换的新荧幕
def update_screen(bg_color, screen, stats, sb, ship, enemies, bullets, play_button):
    # 可能还有个'ai_settings'
    # 在舰船和外星人后面重绘所有子弹
    screen.fill(bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 语句前后位置会影响对象可视时的图像优先级！！！！！！！！！！！！！！！！！！！
    # enemy.blit_me()
    ship.blit_me()
    enemies.draw(screen)
    sb.show_score()
    # 如果游戏处于非活跃状态，就显示play按钮
    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的荧幕可见
    pygame.display.flip()


# 如果敌人到达荧幕边缘时采取相应的措施
def check_fleet_edges(enemies):
    for enemy in enemies.sprites():
        if enemy.check_edges():
            change_fleet_direction(enemies)
            break


# 将整群敌人下移，并改变他们的方向
def change_fleet_direction(enemies):
    for enemy in enemies.sprites():
        enemy.rect.y += fleet_drop_speed
    Enemy.fleet_direction *= -1


# 更新敌人的位置
def update_enemies(screen, stats, sb, ship, enemies, bullets):
    # 检查是否有处于边缘的敌人，更新整群敌人的位置
    check_fleet_edges(enemies)
    enemies.update()

    # 检测舰船与敌人的碰撞
    if pygame.sprite.spritecollideany(ship, enemies):
        ship_hit(screen, stats, sb, ship, enemies, bullets)

    # 检查敌人是否到达底端
    check_enemy_bottom(screen, stats, sb, ship, enemies, bullets)


# 响应子弹与敌人的碰撞,删除发生碰撞的子弹和敌人
def check_bullet_enemy_collisions(screen, stats, sb, ship, enemies, bullets):

    collosions = pygame.sprite.groupcollide(bullets, enemies, True, True)

    if collosions:
        for enemies in collosions.values():
            stats.score += enemy_points * len(enemies)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(enemies) == 0:
        # 删除现有的子弹，并创建新的敌人
        bullets.empty()
        create_fleet(screen, ship, enemies)
        stats.level += 1
        sb.prep_level()


# 响应被敌人撞到的舰船
def ship_hit(screen, stats, sb, ship, enemies, bullets):
    if stats.ships_left > 0:
        # 将ships_left减1
        stats.ships_left -= 1
        sb.prep_ship()
        # 清空敌人列表和子弹列表
        enemies.empty()
        bullets.empty()

        # 创建一群新的敌人，并将舰船归位
        create_fleet(screen, ship, enemies)
        ship.center_ship()

        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


# 检查敌人是否到达了荧幕底端
def check_enemy_bottom(screen, stats, sb, ship, enemies, bullets):
    screen_rect = screen.get_rect()
    for enemy in enemies.sprites():
        if enemy.rect.bottom >= screen_rect.bottom:
            # 将舰船判定为被撞到
            ship_hit(screen, stats, sb, ship, enemies, bullets)
            break


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


enemy_points = 50
