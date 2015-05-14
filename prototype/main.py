import pygame
import time
import thread
import os
import sys
import random
from pygame.locals import *

ALIEN_ROWS = 5
ALIEN_COLUMNS = 11

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

class AlienTwo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.speed = 30  # Speed of alien movement
        self.vector = [1, 1]
        self.has_moved = 0
        self.wait_time = 700
        self.time = pygame.time.get_ticks()

    def update(self):
        if GameState.alien_time - self.time > self.wait_time:
            # width of alien?
            #if self.rect.x >= 0 and self.rect.x <= 1080 - 26:
            if self.has_moved < 22:
                self.rect.x += self.vector[0] * self.speed
                self.has_moved += 1
            else:
                # 20 being the row height?
                self.rect.y += self.vector[1] * 20
                #if self.rect.x > 0:
                #    self.rect.x = 1080 - 26
                #else:
                #    self.rect.x = 0
                self.has_moved = 0
                self.vector[0] *= -1
            self.time = GameState.alien_time

class AlienThree(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.speed = 30  # Speed of alien movement
        self.vector = [1, 1]
        self.has_moved = 0
        self.wait_time = 700
        self.time = pygame.time.get_ticks()

    def update(self):
        if GameState.alien_time - self.time > self.wait_time:
            # width of alien?
            #if self.rect.x >= 0 and self.rect.x <= 1080 - 26:
            if self.has_moved < 22:
                self.rect.x += self.vector[0] * self.speed
                self.has_moved += 1
            else:
                self.rect.y += self.vector[1] * 20
                self.has_moved = 0
                # 20 being the row height?
                #if self.rect.x > 0:
                #    self.rect.x = 1080 - 26
                #else:
                #    self.rect.x = 0
                self.vector[0] *= -1
            self.time = GameState.alien_time

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.speed = 30  # Speed of alien movement
        self.vector = [1, 1]
        self.has_moved = 0
        self.wait_time = 700
        self.time = pygame.time.get_ticks()

    def update(self):
        if GameState.alien_time - self.time > self.wait_time:
            # width of alien?
            #if self.rect.x >= 0 and self.rect.x <= 1080 - 26:
            if self.has_moved < 22:
                self.rect.x += self.vector[0] * self.speed
                self.has_moved += 1
            else:
                # 20 being the row height?
                self.rect.y += self.vector[1] * 20
                #if self.rect.x > 0:
                #    self.rect.x = 1080 - 26
                #else:
                #    self.rect.x = 0
                self.has_moved = 0
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

class Block(pygame.sprite.Sprite):
    def __init__(self, color, (width, height)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

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
        self.make_alien_wave(1)
        self.init_gamestate()

    def init_sprite_groups(self):
        self.player_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.barrier_group = pygame.sprite.Group()
        self.missile_group = pygame.sprite.Group()
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
        sprite = pygame.image.load("assets/images/alien_2a.png")
        sprite = pygame.transform.scale(sprite, (27, 20))
        AlienTwo.image = sprite
        sprite = pygame.image.load("assets/images/alien_3a.png")
        sprite = pygame.transform.scale(sprite, (27, 20))
        AlienThree.image = sprite

    # This should be elsewhere,
    # Maybe its own class.
    def alien_image_type(self, typeOfAlien):
        if (typeOfAlien == 0):
            alien = Alien()
        elif (typeOfAlien == 1):
            alien = AlienTwo()
        elif (typeOfAlien == 2):
            alien = AlienThree()

        self.alien_group.add(alien)
        self.all_sprite_list.add(alien)
        return alien

    def make_alien_wave(self, number):
        for row in range(ALIEN_ROWS):
            for column in range(ALIEN_COLUMNS):
                if row == 0:
                    alien = self.alien_image_type(2)
                elif row == 1 or row == 2:
                    alien = self.alien_image_type(1)
                else:
                    alien = self.alien_image_type(0)

                alien_width = 27
                alien_height = 20
                spacer = 10
                # 27 being the width of one alien
                # 20 being the height of one alien
                # 10 is a spacer
                alien.rect.x = spacer + (
                        column * (alien_width + spacer))
                alien.rect.y = alien_height + (row * (
                    alien_height + spacer))

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
                if event.key == K_SLASH:
                    self.screen = pygame.display.set_mode((1080, 720), DOUBLEBUF | FULLSCREEN)

        keys = pygame.key.get_pressed()
        if keys[K_k]:
            GameState.vector = 1
        elif keys[K_d]:
            GameState.vector = -1
        else:
            GameState.vector = 0

        if keys[K_r] or keys[K_u]:
            GameState.shoot_bullet = True


    def render_screen(self):
        self.all_sprite_list.draw(self.screen)
        pygame.display.update()
        self.screen.blit(self.background, (0,0))
        self.clock.tick(30)

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
                      self.alien_group, self.missile_group]:
            for i in actor:
                i.update()
        if GameState.shoot_bullet:
            self.make_bullet()

    def collision_detection(self):
        pygame.sprite.groupcollide(
                self.missile_group, self.barrier_group, True, True)
        pygame.sprite.groupcollide(
                self.bullet_group, self.barrier_group, True, True)

        if pygame.sprite.groupcollide(
                self.player_group, self.missile_group, False, True):
            print "player loses a life"

        for z in pygame.sprite.groupcollide(
                self.bullet_group, self.alien_group, True, True):
            print "alien should die"
    
    def make_alien_missile(self):
        if len(self.alien_group):
            shoot = random.random()
            if shoot <= 0.01:
                shooter = random.choice([
                    alien for alien in self.alien_group])
                missile = Missile()
                sprite = pygame.image.load("assets/images/missile.png")
                sprite = pygame.transform.scale(sprite, (4, 10))
                missile.image = sprite
                missile.rect = missile.image.get_rect()
                missile.rect.x = shooter.rect.x + 15
                missile.rect.y = shooter.rect.y + 40
                missile.speed = 5
                missile.vector = 1
                self.missile_group.add(missile)
                self.all_sprite_list.add(missile)

    def make_barrier(self, columns, rows, spacer):
        for row in range(rows):
            for column in range(columns):
                barrier = Block((5, 251, 5), (10, 10))
                barrier.rect.x = 110 + (250 * spacer) + (column * 10)
                barrier.rect.y = 600 + (row * 10)
                self.barrier_group.add(barrier)
                self.all_sprite_list.add(barrier)

    def make_defenses(self):
        for spacing, spacing in enumerate(xrange(4)):
            self.make_barrier(9, 3, spacing)

    def main_loop(self):
        self.make_player()
        self.make_defenses()
        while 1:
            GameState.alien_time = pygame.time.get_ticks()
            self.process_input()
            self.make_alien_missile()
            self.collision_detection()
            self.update()
            self.render_screen()

if __name__ == "__main__":
    pyvader = Pyvader()
    pyvader.main_loop()
