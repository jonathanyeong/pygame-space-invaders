import pygame
import thread
import fps

class Player(object):
    def __init__(self, (screen_x, screen_y)):
        self._sprite = pygame.image.load("pyvader/assets/images/player_ship.png")
        self._missile_sprite = pygame.image.load("pyvader/assets/images/missile.png")
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
        # Firing information
        self._missile_sprite = pygame.transform.scale(self._missile_sprite,
                                                      (4, 10))
        self._missile_xpos = self._currX + (self._sprite.get_width() / 2)
        self._missile_ypos = self._currY
        self._missile_speed = 6
        self._is_firing = False

    def get_lives(self):
        return self._lives

    def fire_thread(self):
        clock = fps.Fps()
        while (self._is_firing == True) and (-1*(self._missile_ypos) < 0):
            self._missile_ypos -= self._missile_speed
            clock.tick()

        self._is_firing = False
        self._missile_xpos = self._currX + (self._sprite.get_width() / 2)
        self._missile_ypos = self._currY

    def fire(self):
        if self._is_firing != True:
            # Update missile x, y before starting thread
            self._missile_xpos = self._currX + (self._sprite.get_width() / 2)
            self._missile_ypos = self._currY
            self._is_firing = True
            thread.start_new_thread(self.fire_thread, ())

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

    def render(self, background):
        background.blit(self._sprite, self.position())
        if self._is_firing == True:
            background.blit(self._missile_sprite, (self._missile_xpos,
                                              self._missile_ypos))
        return background 

    # For testing purposes
    def get_speed(self):
        return self._speed
