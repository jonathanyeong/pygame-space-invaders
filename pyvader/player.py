
class Player(object):
    def __init__(self):
        self._lives = 3

    def get_lives(self):
        return self._lives

    def fire(self):
        return True

    def take_damage(self):
        self._lives -= 1
