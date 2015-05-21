import pygame
import random
from gamestate import GameState

class Mothership(pygame.sprite.Sprite):
    def __init__(self, speed, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.max_width = screen_width
        self.speed = speed
        self.rect.topleft = (self.max_width, self.rect.height*2)
        self.time = pygame.time.get_ticks()

    def update(self):
        if self.rect.x > 0 and GameState.mothership_animating:
            self.time = GameState.alien_time
            self.rect.x -= self.speed
        else:
            GameState.shots_taken = 0
            GameState.mothership_animating = False
            self.rect.topleft = (self.max_width, self.rect.height*2)

