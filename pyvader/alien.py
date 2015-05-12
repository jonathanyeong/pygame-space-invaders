import pygame
import alien_type

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        self.sprite_animation = []
        self.sprite_animation.append(pygame.transform.scale(pygame.image.load("assets/images/alien_1a.png"), (27, 20)))
        self.sprite_animation.append(pygame.transform.scale(pygame.image.load("assets/images/alien_1b.png"), (27, 20)))

