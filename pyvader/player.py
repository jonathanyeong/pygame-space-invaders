import pygame
import thread
import fps


class Player(object):
    def __init__(self, (screen_x, screen_y)):
        self.player_sprite = pygame.image.load("pyvader/assets/images/player_ship.png")
        self.missile_sprite = pygame.image.load("pyvader/assets/images/missile.png")
        # Sprite manipulation
        # Ratio between the player is 1.6
        print "x: %d, y: %d" % (screen_x, screen_y)
        player_width = int(screen_x*0.02)
        player_height = int(screen_y*0.02)
        self.player_sprite = pygame.transform.scale(self.player_sprite,
                                                    (player_width, player_height))
        self.missile_sprite = pygame.transform.scale(self.missile_sprite,
                                                     (int(player_width*0.1), int(player_height*0.7)))
        # Other properties
        self.screen_width = screen_x
        self.screen_height = screen_y
        # Player and missile properties
        self.__initial_player_properties()
        self.__initial_missile_properties()

    def __initial_player_properties(self):
        self.currX = self.screen_width/2
        margin = 10  # Arbitrary number
        self.currY = self.screen_height - self.player_sprite.get_rect().height - margin
        self.lives = 3
        self.speed = 100  # Some arbitrary speed of movement

    def __initial_missile_properties(self):
        self.missile_xpos = self.currX + (self.player_sprite.get_width() / 2)
        self.missile_ypos = self.currY
        self.missile_speed = 60
        self.is_firing = False

    def get_lives(self):
        return self.lives

    def fire_thread(self):
        clock = fps.Fps()
        while (self.is_firing is True) and (-1*(self.missile_ypos) < 0):
            self.missile_ypos -= self.missile_speed
            clock.tick()

        self.is_firing = False
        self.missile_xpos = self.currX + (self.player_sprite.get_width() / 2)
        self.missile_ypos = self.currY

    def fire(self):
        if self.is_firing is not True:
            # Update missile x, y before starting thread
            self.missile_xpos = self.currX + (self.player_sprite.get_width() / 2)
            self.missile_ypos = self.currY
            self.is_firing = True
            thread.start_new_thread(self.fire_thread, ())

    def take_damage(self):
        self.lives -= 1

    def position(self):
        return (self.currX, self.currY)

    def move_right(self):
        sprite_width = self.player_sprite.get_rect().width
        if (self.currX < (self.screen_width - sprite_width*1.5)):
            self.currX += self.speed
        return self.position()

    def move_left(self):
        if (self.currX > 0):
            self.currX -= self.speed
        return self.position()

    def render(self, background):
        background.blit(self.player_sprite, self.position())
        if self.is_firing is True:
            background.blit(self.missile_sprite, (self.missile_xpos,
                                                  self.missile_ypos))
        return background

    # For testing purposes
    def get_speed(self):
        return self.speed
