import pygame
from utility import image_loader
from gamestate import GameState

class Alien(pygame.sprite.Sprite):
    def __init__(self, speed, wait_time, row_distance, steps, typeOfAlien):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        if (typeOfAlien == 0):
            self.images.append(image_loader.load_image("assets/images/alien_3a.png"))
            self.images.append(image_loader.load_image("assets/images/alien_3b.png"))
        elif (typeOfAlien == 1 or typeOfAlien == 2):
            self.images.append(image_loader.load_image("assets/images/alien_2a.png"))
            self.images.append(image_loader.load_image("assets/images/alien_2b.png"))
        else:
            self.images.append(image_loader.load_image("assets/images/alien_1a.png"))
            self.images.append(image_loader.load_image("assets/images/alien_1b.png"))
            
        self.index = 0 
        self.image = self.images[self.index]
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
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            if self.has_moved < self.steps:
                self.rect.x += self.vector[0] * self.speed
                self.has_moved += 1
            else:
                self.rect.y += self.vector[1] * self.row_distance
                self.speed += self.speed * 0.2
                self.steps -= self.steps * 0.2
                self.has_moved = 0
                self.vector[0] *= -1
            self.time = GameState.alien_time
