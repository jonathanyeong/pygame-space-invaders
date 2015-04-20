import pygame

class Player(object):
    def __init__(self, (screen_x, screen_y)):
        self._sprite = pygame.image.load("pyvader/assets/images/player_ship.png")
        # Probably need to resize based on screen dimensions
        # Have a break point for scaling
        # if screen_x > some number: Do this scaling
        # Otherwise: Do this scaling
        self._sprite = pygame.transform.scale(self._sprite, (26, 16))
        self._lives = 3
        # Player starts in the middle of the screen
        self._currX = screen_x/2
        margin = 10  # Arbitrary number
        self._currY = screen_y - self._sprite.get_rect().height - margin
        self._speed = 15  # Some arbitrary speed of movement
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
        sprite_width = self._sprite.get_rect().width
        if (self._currX < (self._boundary - sprite_width*1.5)):
            self._currX += self._speed
        return self.position()

    def move_left(self):
        if (self._currX > 0):
            self._currX -= self._speed
        return self.position()

    def render(self):
        return self._sprite, self.position()
