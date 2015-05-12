import pygame
import os
import sys
from pygame.locals import *

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.frame = 0
        self.stop_threads = False
        frame_1 = pygame.image.load("assets/images/alien_1a.png")
        frame_1 = pygame.transform.scale(frame_1, (27, 20))
        frame_2 = pygame.image.load("assets/images/alien_1b.png")
        frame_2 = pygame.transform.scale(frame_2, (27, 20))
        self.images.append(frame_1)
        self.images.append(frame_2)
        self.image = self.images[self.frame]
        self.rect = pygame.Rect(5, 5, 27, 20)

    def update(self):
        self.frame += 1
        if self.frame >= len(self.images):
            self.frame = 0
        self.image = self.images[self.frame]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprite = pygame.image.load("assets/images/player_ship.png")
        self.sprite = pygame.transform.scale(self.sprite, (26, 16))
        self.speed = 10

    def set_position(self, width, height):
        self.width = width
        self.height = height
        self.x = width/2
        self.y = height - self.sprite.get_rect().height - 10

    def get_position(self):
        return (self.x, self.y)

    def move_right(self):
        sprite_width = self.sprite.get_rect().width
        if (self.x < self.width - sprite_width*1.5):
            self.x += self.speed
        return self.get_position()

    def move_left(self):
        if (self.x > 0):
            self.x -= self.speed
        return self.get_position()

    def get_player_layer(self):
        return self.sprite

class Pyvader:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1080, 720), DOUBLEBUF)
        pygame.display.set_caption("Pygame Space Invader Prototype")
        self.screen.fill((10,10,10))
        self.player = Player()
        self.player.set_position(self.screen.get_rect().width, 
                                  self.screen.get_rect().height)
        self.background = pygame.Surface(self.player.get_player_layer().get_size())
        self.background = self.background.convert()
        self.background.fill((10, 10, 10))
        self.alien = Alien()
        self.alien_group = pygame.sprite.Group(self.alien)

        self.run()

    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            keys = pygame.key.get_pressed()
            if keys[K_d]:
                self.player.move_right()
            if keys[K_a]:
                self.player.move_left()
           
            self.screen.fill((10,10,10))
            self.alien_group.update()
            self.alien_group.draw(self.screen)
            self.background.blit(self.player.get_player_layer(),
                                 (0,0))
            self.screen.blit(self.background, self.player.get_position())
            (x,y) = self.player.get_position()
            pygame.display.update(pygame.Rect(x, y, 
                                              self.background.get_rect().width, 
                                              self.background.get_rect().height))

if __name__ == "__main__":
    pyvader = Pyvader()
