import pygame
from alien import Alien
from alien_two import AlienTwo
from alien_three import AlienThree

class AlienManager:
    def __init__(self):
        self.init_alien_sprite()

    def init_alien_sprite(self):
        sprite = pygame.image.load("assets/images/alien_1a.png")
        sprite = pygame.transform.scale(sprite, (27, 20))
        Alien.image = sprite
        sprite = pygame.image.load("assets/images/alien_2a.png")
        sprite = pygame.transform.scale(sprite, (27, 20))
        AlienTwo.image = sprite
        sprite = pygame.image.load("assets/images/alien_3a.png")
        sprite = pygame.transform.scale(sprite, (27, 20))
        AlienThree.image = sprite

    def alien_image_type(self, typeOfAlien):
        if (typeOfAlien == 0):
            alien = Alien()
        elif (typeOfAlien == 1):
            alien = AlienTwo()
        elif (typeOfAlien == 2):
            alien = AlienThree()

        return alien
