#!/usr/bin/python
import pygame
import time
import os
import sys
import random
from gamestate import GameState
from player import Player
from alien import Alien
from alien_two import AlienTwo
from alien_three import AlienThree
from missile import Missile
from alien_manager import AlienManager
from block import Block
from pygame.locals import *

ALIEN_ROWS = 5
ALIEN_COLUMNS = 11
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720
PLAYER_HEIGHT = 26
PLAYER_WIDTH = 16
ALIEN_WIDTH = 27
ALIEN_HEIGHT = 20
PLAYER_LIVES = 1


class Pyvader:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                              DOUBLEBUF)
        pygame.display.set_caption("Pygame Space Invader Prototype")
        self.screen.fill((10, 10, 10))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((10, 10, 10))
        self.clock = pygame.time.Clock()
        self.init_sprite_groups()
        self.init_player_sprite()
        self.init_gamestate()
        self.alien_manager = AlienManager()
        self.alien_manager.init_alien_sprite()
        self.font = pygame.font.Font(None, 42)
        GameState.start_screen = True

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
        self.player_lives = PLAYER_LIVES
        sprite = pygame.image.load("assets/images/player_ship.png")
        sprite = pygame.transform.scale(sprite, (PLAYER_HEIGHT, PLAYER_WIDTH))
        Player.image = sprite

    # ----------------------------------------------------
    #               VIDEO/DISPLAY Methods
    # ----------------------------------------------------

    def splash_screen(self):
        while GameState.start_screen:
            self.main_menu_text()
            logo = pygame.image.load("assets/images/ClearLogo.png")
            bg_center = self.background.get_rect().center
            self.background.blit(logo, logo.get_rect(center=bg_center))
            self.screen.blit(self.background, (0, 0))
            pygame.display.update()
            self.process_input()

    def draw_text(self, render_text, pos):
        text = self.font.render(render_text, 1, (250, 250, 250))
        textpos = text.get_rect()
        (x, y) = pos

        if (y == 0):
            # We know that this is at the top of the screen
            textpos.midtop = pos
        elif (y == self.background.get_rect().height):
            # We know that this is the bottom of screen
            textpos.midbottom = pos
        else:
            textpos.center = pos

        return text, textpos

    def main_menu_text(self):
        # Display title text
        (title_text, textpos) = self.draw_text("Space Invaders",
                                               self.background.get_rect().midtop)
        self.background.blit(title_text, textpos)
        # Display instruction text
        (instruction_text, textpos) = self.draw_text("Press B to start",
                                                     self.background.get_rect().midbottom)
        self.background.blit(instruction_text, textpos)
            
    # ----------------------------------------------------
    #               Sprite Factory Methods
    # ----------------------------------------------------

    # This should be elsewhere,
    # Maybe its own class.
    def alien_image_type(self, typeOfAlien):
        alien = self.alien_manager.alien_image_type(typeOfAlien)
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

                spacer = 10
                # 27 being the width of one alien
                # 20 being the height of one alien
                # 10 is a spacer
                alien.rect.x = spacer + (
                        column * (ALIEN_WIDTH + spacer))
                alien.rect.y = ALIEN_HEIGHT + (row * (
                     ALIEN_HEIGHT + spacer))

    def make_player(self):
        self.player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player_group.add(self.player)
        self.all_sprite_list.add(self.player)
    
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

    def make_alien_missile(self):
        if len(self.alien_group):
            shoot = random.random()
            if shoot <= 0.05:
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
        x_offset = 75
        y_offset = 600
        barrier_spacing = 170
        for row in range(rows):
            for column in range(columns):
                barrier = Block((5, 251, 5), (10, 10))
                barrier.rect.x = x_offset + (barrier_spacing * spacer) \
                                 + (column * 10)
                barrier.rect.y = y_offset + (row * 10)
                self.barrier_group.add(barrier)
                self.all_sprite_list.add(barrier)

    def make_defenses(self):
        barrier_length = 7
        barrier_height = 3
        for spacing, spacing in enumerate(xrange(4)):
            self.make_barrier(barrier_length, barrier_height, spacing)

    # ----------------------------------------------------
    #               Main Loop Methods
    # ----------------------------------------------------
    

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
                    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | FULLSCREEN)

        keys = pygame.key.get_pressed()
        if keys[K_k]:
            GameState.vector = 1
        elif keys[K_d]:
            GameState.vector = -1
        else:
            GameState.vector = 0

        if keys[K_RETURN]:
            if GameState.start_screen:
                GameState.start_screen = False
                self.make_player()
                self.make_alien_wave(1)
                self.make_defenses()

        if keys[K_r] or keys[K_u]:
            GameState.shoot_bullet = True

    def render_screen(self):
        self.background.fill((10, 10, 10))
        self.screen.blit(self.background, (0,0))
        self.all_sprite_list.draw(self.screen)
        pygame.display.update()
        self.clock.tick(30)

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
            self.player_lives -= 1

        for z in pygame.sprite.groupcollide(
                self.bullet_group, self.alien_group, True, True):
            print "alien should die with an explosion! And some sound!"

    def is_dead(self):
        if self.player_lives < 0:
            (title_text, textpos) = self.draw_text("You lost the game!", 
                                                  (self.background.get_rect().center))
            print "title text: ", title_text
            print "text pos: ", textpos
            self.screen.blit(title_text, textpos)
            pygame.display.flip()
            self.reset_game()
            pygame.time.delay(2000)
            return True

    def reset_game(self):
        for items in [self.bullet_group, self.player_group,
                      self.alien_group, self.missile_group,
                      self.barrier_group]:
            for i in items:
                i.kill()
        self.player_lives = PLAYER_LIVES

        
    def main_loop(self):
        while 1:
            if GameState.start_screen:
                self.splash_screen()
            elif not GameState.start_screen:
                GameState.alien_time = pygame.time.get_ticks()
                self.process_input()
                self.make_alien_missile()
                self.collision_detection()
                self.update()
                self.render_screen()
                if self.is_dead():
                    GameState.start_screen = True
                

if __name__ == "__main__":
    pyvader = Pyvader()
    pyvader.main_loop()
