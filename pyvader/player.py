
class Player(object):
    def __init__(self, boundary):
        self._lives = 3
        # Player can only move on X axis
        # Player starts in the middle of the screen
        self._currX = boundary/2
        self._speed = 1  # Some arbitrary speed of movement
        self._boundary = boundary

    def get_lives(self):
        return self._lives

    def fire(self):
        return True

    def take_damage(self):
        self._lives -= 1

    def position(self):
        return self._currX

    def move_right(self):
        if (self._currX < self._boundary):
            self._currX += self._speed
        return self.position()

    def move_left(self):
        if (self._currX > 0):
            self._currX -= self._speed
        return self.position()
