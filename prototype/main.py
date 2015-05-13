import pygame
import time
import thread
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
        time.sleep(0.3)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        # 1080 is screen width
        # 26 is player rect width
        self.rect.x = 1080/2 - 26/2
        self.rect.y = 720 - 26
        self.speed = 10

    def update(self):
        self.rect.x += GameState.vector * self.speed
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > 1080 - 26:
            self.rect.x = 1080 - 26

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.speed = 50  # Speed of alien movement
        self.vector = [1, 1]
        self.wait_time = 900
        self.time = pygame.time.get_ticks()

    def update(self):
        if GameState.alien_time - self.time > self.wait_time:
            # width of alien?
            if self.rect.x >= 0 and self.rect.x <= 1080 - 26:
                self.rect.x += self.vector[0] * self.speed
            else:
                # 20 being the row height?
                self.rect.y += self.vector[1] * 20
                if self.rect.x > 0:
                    self.rect.x = 1080 - 26
                else:
                    self.rect.x = 0
                self.vector[0] *= -1
            self.time = GameState.alien_time

class Missile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.rect = self.image.get_rect()
        self.speed = 0
        self.vector = 0

    def update(self):
        self.rect.y += self.vector * self.speed
        if self.rect.y < 0 or self.rect.y > 720:
            self.kill()

class GameState:
    pass

class Pyvader:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1080, 720), DOUBLEBUF)
        pygame.display.set_caption("Pygame Space Invader Prototype")
        self.screen.fill((10,10,10))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((10, 10, 10))
        self.clock = pygame.time.Clock()
        self.init_sprite_groups()
        self.init_player_sprite()
        self.init_alien_sprite()
        self.init_gamestate()

    def init_sprite_groups(self):
        self.player_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.alien_group = pygame.sprite.Group()
        self.all_sprite_list = pygame.sprite.Group() 

    def init_gamestate(self):
        GameState.vector = 0
        GameState.shoot_bullet = False

    def init_player_sprite(self):
        sprite = pygame.image.load("assets/images/player_ship.png")
        sprite = pygame.transform.scale(sprite, (26, 16))
        Player.image = sprite

    def init_alien_sprite(self):
        sprite = pygame.image.load("assets/images/alien_1a.png")
        sprite = pygame.transform.scale(sprite, (27, 20))
        Alien.image = sprite

    def make_alien_wave(self, number):
        for i in range(0, number):
            alien = Alien()
            alien.rect.x = 0
            alien.rect.y = 0
            self.alien_group.add(alien)
            self.all_sprite_list.add(alien)

    def make_player(self):
        self.player = Player()
        self.player_group.add(self.player)
        self.all_sprite_list.add(self.player)
    
    def process_input(self):
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
            GameState.vector = 1
        elif keys[K_a]:
            GameState.vector = -1
        else:
            GameState.vector = 0

        if keys[K_SPACE]:
            GameState.shoot_bullet = True


    def render_screen(self):
        self.all_sprite_list.draw(self.screen)
        pygame.display.update()
        self.screen.blit(self.background, (0,0))

    def make_bullet(self):
        # This fixes the issue where multiple bullets will keep firing
        # because the keypress is registered multiple times (debouncing issue)
        if len(self.bullet_group) == 0:
            bullet = Missile()
            sprite = pygame.image.load("assets/images/missile.png")
            sprite = pygame.transform.scale(sprite, (4, 10))
            bullet.image = sprite
            bullet.rect = bullet.image.get_rect()
            bullet.vector = -1
            bullet.speed = 10
            bullet.rect.x = self.player.rect.x + 10
            bullet.rect.y = self.player.rect.y
            self.bullet_group.add(bullet)
            self.all_sprite_list.add(bullet)
        GameState.shoot_bullet = False

    def update(self):
        for actor in [self.player_group, self.bullet_group,
                      self.alien_group]:
            for i in actor:
                i.update()
        if GameState.shoot_bullet:
            self.make_bullet()

    def main_loop(self):
        self.make_player()
        self.make_alien_wave(1)
        while 1:
            GameState.alien_time = pygame.time.get_ticks()
            self.process_input()
            self.update()
            self.render_screen()

if __name__ == "__main__":
    pyvader = Pyvader()
    pyvader.main_loop()
