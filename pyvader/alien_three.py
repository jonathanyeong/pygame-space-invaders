import pygame
from gamestate import GameState

class AlienThree(pygame.sprite.Sprite):
    def __init__(self, speed, wait_time, row_distance, steps):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.speed = speed  # Speed of alien movement
        self.row_distance = row_distance
        self.vector = [1, 1]
        self.has_moved = 0
        self.wait_time = wait_time
        self.time = pygame.time.get_ticks()
        self.steps = steps

    def update(self):
        if GameState.alien_time - self.time > self.wait_time:
            # width of alien?
            #if self.rect.x >= 0 and self.rect.x <= 1080 - 26:
            if self.has_moved < self.steps:
                self.rect.x += self.vector[0] * self.speed
                self.has_moved += 1
            else:
                # 20 being the row height?
                self.rect.y += self.vector[1] * self.row_distance
                #if self.rect.x > 0:
                #    self.rect.x = 1080 - 26
                #else:
                #    self.rect.x = 0
                self.has_moved = 0
                self.vector[0] *= -1
            self.time = GameState.alien_time
