import pygame
from gamestate import GameState

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.max_width = screen_width
        # 1080 is screen width
        # 26 is player rect width
        self.rect.x = screen_width/2 - 26/2
        self.rect.y = screen_height - 26
        self.speed = 10

    def update(self):
        self.rect.x += GameState.vector * self.speed
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > self.max_width - 26:
            self.rect.x = self.max_width - 26
