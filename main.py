import pygame
import sys
from player import Player
from game_platform import Platform
from block import Block
from flag import Flag

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

player = Player(100, 100, screen_width, screen_height)
platform = Platform(0, screen_height - 40, screen_width, 40)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(platform)

# プラットフォームの作成
ground = Platform(0, screen_height - 40, screen_width, 40)

# プラットフォームをグループに追加
platform_group = pygame.sprite.Group()
platform_group.add(ground)

# all_sprites グループにもプラットフォームを追加
all_sprites.add(ground)


# ブロックの作成
block1 = Block(200, screen_height - 180, 40, 40)

# ブロックをグループに追加
block_group = pygame.sprite.Group()
block_group.add(block1)

# all_sprites グループにもブロックを追加
all_sprites.add(block1)

# 旗の作成
flag = Flag(700, screen_height - 140, 35, 100)

# 旗をグループに追加
flag_group = pygame.sprite.Group()
flag_group.add(flag)

# all_sprites グループにも旗を追加
all_sprites.add(flag)

# フォントオブジェクトを作成
pygame.font.init()
font = pygame.font.Font(None, 36)

reset_text = font.render("R: Clear", True, (0, 0, 0))

pause = False
pause_text = font.render("P: Pause", True, (0, 0, 0))

quit_text = font.render("Q: Quit", True, (0, 0, 0))

# ゲーム開始時の時刻を取得
start_time = pygame.time.get_ticks()
pause_start_time = 0
pause_duration = 0

# ゴールした時刻を保存するリスト
goal_times = []

# ブロックを触った時間を保存するリスト
block_touch_times = []
last_block_touch_time = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
                # P キーが押されたら一時停止状態を切り替える
                if event.key == pygame.K_p:
                    pause = not pause
                    # 一時停止状態の場合、更新処理をスキップする
                    if pause:
                        # 一時停止が開始された時刻を保存
                        pause_start_time = pygame.time.get_ticks()
                    else:
                        # 一時停止が終了したら、一時停止にかかった時間を計算し、start_time に加算
                        pause_duration += pygame.time.get_ticks() - pause_start_time
                # Q キーが押されたら終了
                elif event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_r:
                    goal_times = []
                    block_touch_times = []

    if not pause:
        # 経過時間を計算（ミリ秒単位を秒単位に変換）
        elapsed_time = (pygame.time.get_ticks() - start_time - pause_duration) / 1000
        # 空中にいるときはon_groundフラグをFalseに設定
        player.on_ground = False

        # プレイヤーと地面の衝突を検出
        if pygame.sprite.collide_rect(player, ground):
            player.speed_y = 0
            player.rect.bottom = ground.rect.top
            player.on_ground = True

        player.update()

        # プレイヤーとブロックの衝突を検出
        collisions = pygame.sprite.spritecollide(player, block_group, False)
        for block in collisions:
                # 上向きの速度の場合のみ衝突を処理
                if player.speed_y < 0:
                    player.speed_y = 0
                    player.rect.top = block.rect.bottom
                    block.hit()  # ブロックを叩いた効果を適用
                    
                    # 経過時間を block_touch_times リストに追加
                    block_touch_times.append(elapsed_time - last_block_touch_time)
                    last_block_touch_time = elapsed_time
                # 下向きの速度でブロックの上に衝突
                elif player.speed_y > 0:
                    player.speed_y = 0
                    player.rect.bottom = block.rect.top
                    player.on_ground = True
                # 横方向にブロックに衝突
                else:
                    # プレイヤーがブロックの右から衝突
                    if player.speed_x > 0:
                        player.rect.right = block.rect.left
                    # プレイヤーがブロックの左から衝突
                    elif player.speed_x < 0:
                        player.rect.left = block.rect.right

        # プレイヤーと旗の衝突を検出
        collisions = pygame.sprite.spritecollide(player, flag_group, False)
        if collisions:  # 衝突がある場合
            # ゲームをリセットするための処理を記述
            player.rect.x = 0
            player.rect.y = screen_height
            player.speed_x = 0
            player.speed_y = 0

            # 経過時間を goal_times リストに追加
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

        # 更新
        all_sprites.update()

    # 描画
    screen.fill((135, 206, 235))
    all_sprites.draw(screen)

    # 経過時間のテキストを描画
    time_text = font.render(f"Time: {elapsed_time:.2f}s", True, (0, 0, 0))
    screen.blit(time_text, (10, 10))

    # キーガイドを表示
    screen.blit(reset_text, (screen_width - 100, 0))
    screen.blit(pause_text, (screen_width - 100, 20))
    screen.blit(quit_text, (screen_width - 100, 40))

    # ゴールした時刻を表示
    for i, goal_time in enumerate(goal_times, 1):
        goal_text = font.render(f"[{i}]: {goal_time:.2f}s", True, (0, 0, 0))
        screen.blit(goal_text, (10, 10 + 40 * i))

    # ブロックを触った時間を表示
    for i, block_touch_time in enumerate(block_touch_times, 1):
        touch_text = font.render(f"[{i}]: {block_touch_time:.2f}s", True, (0, 0, 0))
        # テキストの幅を取得
        text_width = touch_text.get_rect().width  
        screen.blit(touch_text, (200, 10 + 40 * i))

    pygame.display.flip()

pygame.quit()
sys.exit()
