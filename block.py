import pygame
import random

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 204, 0))  # ブロックの色を黄色に設定
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def hit(self):
        # ランダムな色を生成
        random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # ブロックの色をランダムな色に変更
        self.image.fill(random_color)
