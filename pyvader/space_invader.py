#!/usr/bin/python
import os
import sys
import pygame
import player
import barricade
from IPython import embed
from pygame.locals import *


class SpaceInvader(object):
    def __init__(self):
        pygame.init()
        # Initialise screen
        self.screen = pygame.display.set_mode((0,0), pygame.DOUBLEBUF | pygame.FULLSCREEN)
        pygame.display.set_caption("PyGame Space Invaders clone")
        pygame.mouse.set_visible(0)
        pygame.key.set_repeat(10, 10)

        # Fill background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((10, 10, 10))

        # Init player
        (max_width, max_height) = self.screen.get_size()
        # We need to take into account the size of the player sprite.
        self.player = player.Player((max_width, max_height))
        self.barricade = barricade.Barricade()
        self.font = pygame.font.Font(None, 42)  # Init some font object

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

    def run(self):
        # Worry about FPS tick later
        START_GAME = False  # ie Main Menu
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        bg_center = self.background.get_rect().center
        # Event loop
        while 1:
            if START_GAME is False:
                self.main_menu_text()
                logo = pygame.image.load("pyvader/assets/images/ClearLogo.png")

                for event in pygame.event.get():
                    if event.type == QUIT:
                        return
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            return
                        if event.key == K_b:
                            print "start game"
                            START_GAME = True
                            break
                        # Option to load full screen as well

                self.background.blit(logo, logo.get_rect(center=bg_center))
                self.screen.blit(self.background, (0, 0))
                pygame.display.flip()
            elif START_GAME is True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        return
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            return
                keys = pygame.key.get_pressed()
                if keys[K_d]:
                    self.player.move_right()
                if keys[K_a]:
                    self.player.move_left()
                if keys[K_SPACE]:
                    self.player.fire()
                # I blit everything onto the background rather than the screen
                self.background.fill((10, 10, 10))
                player_layer = self.player.render(self.background)
                barricade_layer = self.barricade.render(self.background, (300, 300))
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(player_layer, (0, 0))
                pygame.display.flip()

if __name__ == '__main__':
    game = SpaceInvader().run()
