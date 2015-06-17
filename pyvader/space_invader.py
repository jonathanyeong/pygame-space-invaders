#!/usr/bin/python
import pygame
import time
import os
import sys
import random
from gamestate import GameState
from player import Player
from alien import Alien
from mothership import Mothership
from missile import Missile
from alien_manager import AlienManager
from block import Block
from score_tracker import ScoreTracker
from menu import *
from pygame.locals import *

ALIEN_ROWS = 5
ALIEN_COLUMNS = 11
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 500
PLAYER_HEIGHT = 26
PLAYER_WIDTH = 16
ALIEN_WIDTH = 27
ALIEN_HEIGHT = 20
PLAYER_LIVES = 3
BARRIER_BOUNDARY = SCREEN_HEIGHT - 120


class Pyvader:
    def __init__(self, opts):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                              DOUBLEBUF)
        for o, a in opts:
            if o == "-f":
                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                                       DOUBLEBUF | FULLSCREEN)
        pygame.display.set_caption("Pygame Space Invader Prototype")
        self.screen.fill((10, 10, 10))
        self.clock = pygame.time.Clock()
        self.alien_manager = AlienManager()
        self.font = pygame.font.Font(None, 42)
        GameState.start_screen = True
        GameState.score_screen = False
        self.set_background()
        self.init_gamestate()
        self.init_sprites()
        self.init_sfx()
        self.init_explosions()
        self.init_menu()
        self.score_tracker = ScoreTracker()
        pygame.event.set_blocked(pygame.MOUSEMOTION)

    def init_menu(self):
        screen_center = self.screen.get_rect().center
        self.menu = cMenu(screen_center[0], screen_center[1]+100, 20, 5, 'vertical', 100, self.screen,
                        [('Start Game', 1, None),
                         ('High Scores', 2, None),
                         ('Exit Game', 3, None)])
        self.score_menu = cMenu(screen_center[0], screen_center[1]+100, 20, 5, 'vertical', 100, self.screen,
                              [('Back', 0, None)])
        self.menu.set_center(True, False)
        self.menu.set_alignment('center', 'center')
        # States are used for the menu
        self.state = 0
        self.prev_state = 1
        self.rect_list = []

    def init_explosions(self):
        self.explode = False
        self.alien_explode = False
        self.init_player_explosion()
        self.init_alien_explosion()

    def init_sfx(self):
        self.bullet_fx = pygame.mixer.Sound('assets/sounds/shoot.wav')
        self.bullet_fx.set_volume(0.3)
        self.player_explosion_fx = pygame.mixer.Sound('assets/sounds/explosion.wav')
        self.alien_explosion_fx = pygame.mixer.Sound('assets/sounds/invaderkilled.wav')
        self.alien_explosion_fx.set_volume(0.1)

    def set_background(self):
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((10, 10, 10))

    def init_sprites(self):
        self.init_sprite_groups()
        self.init_player_sprite()
        self.init_mothership_sprite()
        self.alien_manager.init_alien_sprite()

    def init_sprite_groups(self):
        self.player_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.barrier_group = pygame.sprite.Group()
        self.missile_group = pygame.sprite.Group()
        self.alien_group = pygame.sprite.Group()
        self.all_sprite_list = pygame.sprite.Group()
        self.mothership_group = pygame.sprite.Group()

    def init_gamestate(self):
        self.score = 0
        self.rounds_won = 0
        GameState.shots_taken = 0
        GameState.vector = 0
        GameState.shoot_bullet = False
        GameState.mothership_animating = False

    def init_player_sprite(self):
        self.player_lives = PLAYER_LIVES
        sprite = pygame.image.load("assets/images/player_ship.png")
        sprite = pygame.transform.scale(sprite, (PLAYER_HEIGHT, PLAYER_WIDTH))
        Player.image = sprite

    def init_mothership_sprite(self):
        sprite = pygame.image.load("assets/images/mothership.png")
        sprite = pygame.transform.scale(sprite, (60, 20))
        Mothership.image = sprite

    def init_bullet(self):
        bullet = Missile()
        sprite = pygame.image.load("assets/images/missile.png")
        sprite = pygame.transform.scale(sprite, (4, 10))
        bullet.image = sprite
        bullet.rect = bullet.image.get_rect()
        bullet.vector = -1
        bullet.speed = 10
        bullet.rect.x = self.player.rect.x + 10
        bullet.rect.y = self.player.rect.y
        return bullet

    def init_alien_missile(self, shooter):
        missile = Missile()
        sprite = pygame.image.load("assets/images/missile.png")
        sprite = pygame.transform.scale(sprite, (4, 10))
        missile.image = sprite
        missile.rect = missile.image.get_rect()
        missile.rect.x = shooter.rect.x + 15
        missile.rect.y = shooter.rect.y + 40
        missile.speed = 5
        missile.vector = 1
        return missile

    def init_player_explosion(self):
        img = pygame.image.load("assets/images/player_destroyed.png")
        img = pygame.transform.scale(img, (PLAYER_HEIGHT, PLAYER_WIDTH))
        self.explosion_img = img

    def init_alien_explosion(self):
        img = pygame.image.load("assets/images/explosion.png")
        img = pygame.transform.scale(img, (ALIEN_WIDTH, ALIEN_HEIGHT))
        self.alien_explosion_img = img
        self.explodey_alien = []  # The alien that was destroyed
        self.alien_explode_pos = 0

    # ----------------------------------------------------
    #               VIDEO/DISPLAY Methods
    # ----------------------------------------------------


    def draw_text(self, render_text, pos, background=None):
        if background is None:
            text = self.font.render(render_text, 1, (250, 250, 250))
        else:
            text = self.font.render(render_text, 1, (250, 250, 250),
                                    background)
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

    # ----------------------------------------------------
    #               Sprite Factory Methods
    # ----------------------------------------------------

    def make_alien_wave(self, speed):
        for row in range(ALIEN_ROWS):
            for column in range(ALIEN_COLUMNS):
                alien = self.alien_manager.alien_image_type(row, speed)
                self.alien_group.add(alien)
                self.all_sprite_list.add(alien)
                spacer = 10
                alien.rect.x = spacer + (
                        column * (ALIEN_WIDTH + spacer))
                alien.rect.y = (3 * ALIEN_HEIGHT) + (row * (
                     ALIEN_HEIGHT + spacer))

    def make_player(self):
        self.player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player_group.add(self.player)
        self.all_sprite_list.add(self.player)

    def make_mothership(self):
        self.mothership = Mothership(1, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.mothership_group.add(self.mothership)
        self.all_sprite_list.add(self.mothership)

    def make_bullet(self):
        # This fixes the issue where multiple bullets will keep firing
        # because the keypress is registered multiple times (debouncing issue)
        if len(self.bullet_group) == 0:
            self.bullet_fx.play()
            GameState.shots_taken += 1
            bullet = self.init_bullet()
            self.bullet_group.add(bullet)
            self.all_sprite_list.add(bullet)
        GameState.shoot_bullet = False

    def make_alien_missile(self):
        if len(self.alien_group):
            shoot = random.random()
            if shoot <= 0.03:
                shooter = random.choice([
                    alien for alien in self.alien_group])
                missile = self.init_alien_missile(shooter)
                self.missile_group.add(missile)
                self.all_sprite_list.add(missile)

    def make_barrier(self, columns, rows, spacer):
        x_offset = 75
        y_offset = BARRIER_BOUNDARY
        barrier_spacing = 170
        block_colour = (5, 251, 5)  # Bright green colour
        block_size = (10, 10)
        for row in range(rows):
            for column in range(columns):
                barrier = Block(block_colour, block_size)
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
    #               Game Logic Methods
    # ----------------------------------------------------

    def is_dead(self):
        if self.player_lives < 1:
            self.lose_game_text()
            pygame.time.delay(2000)
            return True

    def lose_game_text(self):
            (title_text, textpos) = self.draw_text("You lost the game!",
                                                   (self.background.get_rect().center),
                                                   (100, 100, 100))
            self.screen.blit(title_text, textpos)
            pygame.display.flip()


    def win_round(self):
        if len(self.alien_group) < 1:
            self.rounds_won += 1
            (title_text, textpos) = self.draw_text("You won round %d!" % self.rounds_won,
                                                   (self.background.get_rect().center),
                                                   (100, 100, 100))
            self.screen.blit(title_text, textpos)
            pygame.display.flip()
            pygame.time.delay(2000)
            return True

    def next_round(self):
        for actor in [self.missile_group, self.barrier_group,
                      self.bullet_group]:
            for i in actor:
                i.kill()
        self.player_lives = PLAYER_LIVES
        self.make_alien_wave(self.rounds_won)
        self.make_mothership()
        self.make_defenses()

    def defenses_breached(self):
        for alien in self.alien_group:
            if alien.rect.y > BARRIER_BOUNDARY:
                self.lose_game_text()
                pygame.time.delay(2000)
                return True

    # ----------------------------------------------------
    #               Main Loop Methods
    # ----------------------------------------------------
    def reset_game(self):
        for items in [self.bullet_group, self.player_group,
                      self.alien_group, self.missile_group,
                      self.barrier_group]:
            for i in items:
                i.kill()
        self.player_lives = PLAYER_LIVES
        self.rounds_won = 0
        GameState.shots_taken = 0
        self.time = pygame.time.get_ticks()
        GameState.start_screen = False
        self.score = 0
        self.make_player()
        self.make_mothership()
        self.make_alien_wave(1)
        self.make_defenses()

    # Score screen and splash screen should only render the text
    # It shouldn't be doing any processing
    def score_screen(self):
        self.clear_screen()
        #print "scores: ", self.score_tracker.top_five()
        (title_text, textpos) = self.draw_text("High score",
                                            self.background.get_rect().midtop)
        self.screen.blit(title_text, textpos)
        pygame.display.update(self.rect_list)
        #print "score screen"
        #print self.rect_list
        #print "state: %d , previous state %d"%(self.state, self.prev_state)
        if self.prev_state != self.state:
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
            self.prev_state = self.state
        #pygame.display.update(self.rect_list)

    def splash_screen(self):
        self.main_menu_text()
        logo = pygame.image.load("assets/images/ClearLogo.png")
        bg_center = self.background.get_rect().center
        self.screen.blit(logo, logo.get_rect(center=(bg_center[0], bg_center[1] - (logo.get_rect().height/2))))
        if self.prev_state != self.state:
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
            self.prev_state = self.state
        pygame.display.update(self.rect_list)

    def process_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN or event.type == EVENT_CHANGE_STATE:
                if GameState.start_screen:
                    print "state: ", self.state
                    if self.state == 0:
                        self.rect_list, self.state = self.menu.update(event, self.state)
                        print "rect list len: ", len(self.rect_list)
                    elif self.state == 1:
                        self.reset_game()
                        self.state = 0
                    elif self.state == 2:
                        self.rect_list, self.state = self.score_menu.update(event, self.state)
                        print "rect list len: ", len(self.rect_list)
                        GameState.score_screen = True
                    else:
                        pygame.quit()
                        sys.exit()
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_SLASH:
                    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                                          DOUBLEBUF | FULLSCREEN)
        
        if not GameState.start_screen:
            keys = pygame.key.get_pressed()
            if keys[K_k]:
                GameState.vector = 1
            elif keys[K_d]:
                GameState.vector = -1
            else:
                GameState.vector = 0
            if keys[K_r] or keys[K_u]:
                GameState.shoot_bullet = True

    def player_explosion(self):
        if self.explode:
            self.screen.blit(self.explosion_img, [self.player.rect.x, self.player.rect.y])
            self.player_explosion_fx.play()
            pygame.display.update()
            self.explode = False
            time.sleep(1)

    def alien_explosion(self):
        if self.alien_explode:
            if self.alien_explode_pos < 9:
                self.screen.blit(self.alien_explosion_img, [int(self.explodey_alien[0]), int(self.explodey_alien[1])])
                pygame.display.update()
                self.alien_explode_pos += 1
                self.alien_explosion_fx.play()
            else:
                self.alien_explode = False
                self.alien_explode_pos = 0
                self.explodey_alien = []

    def render_screen(self):
        self.background.fill((10, 10, 10))
        self.player_explosion()
        self.alien_explosion()
        self.screen.blit(self.background, (0, 0))
        self.all_sprite_list.draw(self.screen)
        self.refresh_scores()
        pygame.display.update()
        self.clock.tick(30)

    def refresh_scores(self):
        (text, textpos) = self.draw_text(("Lives: %d" % self.player_lives),
                                         self.background.get_rect().midtop)
        (bg_x, bg_y) = self.background.get_rect().topright
        self.screen.blit(text, ((bg_x - text.get_rect().width), bg_y))
        (text, textpos) = self.draw_text(("Score: %d pts" % self.score),
                                         self.background.get_rect().midtop)
        (bg_x, bg_y) = self.background.get_rect().topleft
        self.screen.blit(text, (bg_x, bg_y))

    def update(self):
        for actor in [self.player_group, self.bullet_group,
                      self.alien_group, self.missile_group,
                      self.mothership_group]:
            for i in actor:
                i.update()

        if GameState.mothership_animating is True:
            for actor in self.mothership_group:
                actor.update()

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
            self.explode = True

        for z in pygame.sprite.groupcollide(
                self.alien_group, self.bullet_group, True, True):
            if z.__class__.__name__ == "Alien":
                self.score += 10
            elif z.__class__.__name__ == "AlienTwo":
                self.score += 20
            elif z.__class__.__name__ == "AlienThree":
                self.score += 40

            self.alien_explode = True
            self.explodey_alien.append(z.rect.x)
            self.explodey_alien.append(z.rect.y)

        for z in pygame.sprite.groupcollide(
                self.mothership_group, self.bullet_group, True, True):
            if GameState.shots_taken <= 23:
                self.score += 300
            elif GameState.shots_taken > 23 and GameState.shots_taken <= 33:
                self.score += 150
            elif GameState.shots_taken > 33 and GameState.shots_taken <= 43:
                self.score += 100
            else:
                self.score += 50
            GameState.shots_taken = 0

    def clear_screen(self):
        self.background.fill((10, 10, 10))
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()

    def main_loop(self):
        while 1:
            if GameState.start_screen:
                if not GameState.score_screen:
                    self.splash_screen()
                else:
                    self.score_screen()
                self.process_input()
            elif not GameState.start_screen:
                GameState.alien_time = pygame.time.get_ticks()
                GameState.mothership_time = pygame.time.get_ticks()
                self.process_input()
                self.make_alien_missile()
                self.collision_detection()
                self.update()
                self.render_screen()
                # mothership appears every 25 seconds
                if GameState.mothership_time - self.time > 25000:
                    GameState.mothership_animating = True
                    if (len(self.mothership_group) == 0):
                        self.make_mothership()
                    self.time = GameState.mothership_time
                if self.is_dead() or self.defenses_breached():
                    GameState.start_screen = True
                    self.score_tracker.save_score(self.score)
                    self.clear_screen()
                if self.win_round():
                    self.next_round()


if __name__ == "__main__":
    pyvader = Pyvader()
    pyvader.main_loop()
