import pygame
import sys
from player import Player
from game_platform import Platform
from block import Block
from flag import Flag
from typing import List, Tuple

def handle_events():
    global running, pause, pause_start_time, pause_duration, goal_times, block_touch_times
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = not pause
                    if pause:
                        pause_start_time = pygame.time.get_ticks()
                    else:
                        pause_duration += pygame.time.get_ticks() - pause_start_time
                elif event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_r:
                    goal_times = []
                    block_touch_times = []

def update_game():
    global elapsed_time, last_block_touch_time
    elapsed_time = (pygame.time.get_ticks() - start_time - pause_duration) / 1000
    player.on_ground = False

    if pygame.sprite.collide_rect(player, ground):
        player.speed_y = 0
        player.rect.bottom = ground.rect.top
        player.on_ground = True

    player.update()
    collisions = pygame.sprite.spritecollide(player, block_group, False)
    for block in collisions:
        if player.speed_y < 0:
            player.speed_y = 0
            player.rect.top = block.rect.bottom
            block.hit()  
            block_touch_times.append(elapsed_time - last_block_touch_time)
            last_block_touch_time = elapsed_time
        elif player.speed_y > 0:
            player.speed_y = 0
            player.rect.bottom = block.rect.top
            player.on_ground = True
        else:
            if player.speed_x > 0:
                player.rect.right = block.rect.left
            elif player.speed_x < 0:
                player.rect.left = block.rect.right

    collisions = pygame.sprite.spritecollide(player, flag_group, False)
    if collisions:  
        player.rect.x = 0
        player.rect.y = screen_height
        player.speed_x = 0
        player.speed_y = 0
        goal_times.append(elapsed_time)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    elif keys[pygame.K_RIGHT]:
        player.move_right()
    else:
        player.stop()

    if keys[pygame.K_SPACE]:
        player.jump()

    all_sprites.update()

def draw_game():
    screen.fill((135, 206, 235))
    all_sprites.draw(screen)

    time_text = font.render(f"Time: {elapsed_time:.2f}s", True, (0, 0, 0))
    screen.blit(time_text, (10, 10))

    screen.blit(reset_text, (screen_width - 100, 0))
    screen.blit(pause_text, (screen_width - 100, 20))
    screen.blit(quit_text, (screen_width - 100, 40))

    for i, goal_time in enumerate(goal_times, 1):
        goal_text = font.render(f"[{i}]: {goal_time:.2f}s", True, (0, 0, 0))
        screen.blit(goal_text, (10, 10 + 40 * i))

    for i, block_touch_time in enumerate(block_touch_times, 1):
        touch_text = font.render(f"[{i}]: {block_touch_time:.2f}s", True, (0, 0, 0))
        screen.blit(touch_text, (200, 10 + 40 * i))

    pygame.display.flip()

pygame.init()

screen_width: int = 800
screen_height: int = 600
screen: pygame.Surface = pygame.display.set_mode((screen_width, screen_height))

player: Player = Player(100, 100, screen_width, screen_height)
platform: Platform = Platform(0, screen_height - 40, screen_width, 40)

all_sprites: pygame.sprite.Group = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(platform)

ground: Platform = Platform(0, screen_height - 40, screen_width, 40)
platform_group: pygame.sprite.Group = pygame.sprite.Group()
platform_group.add(ground)
all_sprites.add(ground)

block1: Block = Block(200, screen_height - 180, 40, 40)
block_group: pygame.sprite.Group = pygame.sprite.Group()
block_group.add(block1)
all_sprites.add(block1)

flag: Flag = Flag(700, screen_height - 140, 35, 100)
flag_group: pygame.sprite.Group = pygame.sprite.Group()
flag_group.add(flag)
all_sprites.add(flag)

pygame.font.init()
font: pygame.font.Font = pygame.font.Font(None, 36)

reset_text: pygame.Surface = font.render("R: Clear", True, (0, 0, 0))
pause_text: pygame.Surface = font.render("P: Pause", True, (0, 0, 0))
quit_text: pygame.Surface = font.render("Q: Quit", True, (0, 0, 0))

start_time: int = pygame.time.get_ticks()
pause_start_time: int = 0
pause_duration: int = 0
goal_times: List[float] = []
block_touch_times: List[float] = []
last_block_touch_time: float = 0

running: bool = True
pause: bool = False

while running:
    handle_events()
    if not pause:
        update_game()
    draw_game()

pygame.quit()
sys.exit()
