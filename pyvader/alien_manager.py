import pygame
from alien import Alien
from alien_two import AlienTwo
from alien_three import AlienThree

class AlienManager:
    def __init__(self):
        self.init_alien_sprite()

    def init_alien_sprite(self):
        pass

    def alien_image_type(self, typeOfAlien, speed_multiplier):
        speed = 20 
        wait_time = 1500 - (50 * (speed_multiplier - 1))
        row_distance = 40
        steps = 15
        if (typeOfAlien == 0):
            alien = AlienThree(speed, wait_time, row_distance, steps)
        elif (typeOfAlien == 1 or typeOfAlien == 2):
            alien = AlienTwo(speed, wait_time, row_distance, steps)
        else:
            alien = Alien(speed, wait_time, row_distance, steps)

        return alien
