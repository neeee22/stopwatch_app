import pygame

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # 白い竿を描画
        pygame.draw.rect(self.image, (255, 255, 255), (width//2 -4, 0, 4, height))
        
        # 赤い旗を描画
        pygame.draw.polygon(self.image, (255, 0, 0), [(width // 2 + 18, 25), (width - 18, 0), (width - 18, 50)])
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
