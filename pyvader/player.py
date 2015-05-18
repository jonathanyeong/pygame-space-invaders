import pygame
from gamestate import GameState

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        # 1080 is screen width
        # 26 is player rect width
        self.rect.x = 1080/2 - 26/2
        self.rect.y = 720 - 26
        self.speed = 10

    def update(self):
        self.rect.x += GameState.vector * self.speed
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > 1080 - 26:
            self.rect.x = 1080 - 26
