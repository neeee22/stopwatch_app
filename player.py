import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width, screen_height):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, (255, 255, 0), (25, 25), 25)
        pygame.draw.circle(self.image, (0, 0, 0), (15, 20), 5)
        pygame.draw.circle(self.image, (0, 0, 0), (35, 20), 5)
        
        num_points = 50
        points = []
        for i in range(num_points // 2):
            angle = i * (2 * math.pi) / num_points
            x = 25 + 15 * math.cos(angle)
            y = 35 + 10 * math.sin(angle)
            points.append((x, y))
        pygame.draw.lines(self.image, (0, 0, 0), False, points, 2)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed_x = 0
        self.speed_y = 0
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.on_ground = False

    def update(self):
        # 重力
        self.speed_y += 0.5
        self.rect.y += self.speed_y

        # 水平方向の移動を反映
        self.rect.x += self.speed_x

        # 画面範囲内にプレイヤーを制限
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.screen_width:
            self.rect.right = self.screen_width

        # 画面下部に到達した場合の処理（オプション）
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height
            self.speed_y = 0

    def move_left(self):
        self.speed_x = -3

    def move_right(self):
        self.speed_x = 3

    def stop(self):
        self.speed_x = 0

    def jump(self):
        if self.on_ground:
            self.speed_y = -15