import pygame

class Player(object):
    def __init__(self, (screen_x, screen_y)):
        self._sprite = pygame.image.load("pyvader/assets/images/player_ship.png")
        self._lives = 3
        # Player can only move on X axis
        # Player starts in the middle of the screen
        self._currX = screen_x/2
        self._currY = screen_y
        self._speed = 1  # Some arbitrary speed of movement
        self._boundary = screen_x 

    def get_lives(self):
        return self._lives

    def fire(self):
        return True

    def take_damage(self):
        self._lives -= 1

    def position(self):
        return (self._currX, self._currY)

    def move_right(self):
        if (self._currX < self._boundary):
            self._currX += self._speed
        return self.position()

    def move_left(self):
        if (self._currX > 0):
            self._currX -= self._speed
        return self.position()
