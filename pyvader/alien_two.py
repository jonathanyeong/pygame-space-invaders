import pygame
import gamestate

class AlienTwo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.speed = 30  # Speed of alien movement
        self.vector = [1, 1]
        self.has_moved = 0
        self.wait_time = 1500 
        self.time = pygame.time.get_ticks()

    def update(self):
        if GameState.alien_time - self.time > self.wait_time:
            # width of alien?
            #if self.rect.x >= 0 and self.rect.x <= 1080 - 26:
            if self.has_moved < 22:
                self.rect.x += self.vector[0] * self.speed
                self.has_moved += 1
            else:
                # 20 being the row height?
                self.rect.y += self.vector[1] * 40 
                #if self.rect.x > 0:
                #    self.rect.x = 1080 - 26
                #else:
                #    self.rect.x = 0
                self.has_moved = 0
                self.vector[0] *= -1
            self.time = GameState.alien_time
