import pygame
from alien import Alien

class AlienManager:
    def __init__(self):
        self.init_alien_sprite()

    def init_alien_sprite(self):
        pass

    def alien_image_type(self, typeOfAlien, speed_multiplier):
        speed = 20 
        # Speed multiplier here is used when a new round starts
        wait_time = 1500 - (50 * (speed_multiplier - 1))
        row_distance = 30
        steps = 15
        alien = Alien(speed, wait_time, row_distance, steps, typeOfAlien)
        return alien
