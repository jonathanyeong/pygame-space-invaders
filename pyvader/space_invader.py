#!/usr/bin/python

import os
import sys
import pygame
import player
from IPython import embed
from pygame.locals import *


class SpaceInvader(object):
    def __init__(self):
        pygame.init()
        # Initialise screen
        self.screen = pygame.display.set_mode((600, 480))
        pygame.display.set_caption("PyGame Space Invaders clone")

        # Fill background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((10, 10, 10))

        # Init player
        (max_width, max_height) = self.screen.get_size()
        # We need to take into account the size of the player sprite.
        self.player = player.Player((max_width, max_height))
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
        self.main_menu_text()
        logo = pygame.image.load("assets/images/ClearLogo.png")
        # Blit everything to the screen
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        bg_center = self.background.get_rect().center
        # Event loop
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                keys = pygame.key.get_pressed()

                if keys[K_ESCAPE]:
                    return

            self.screen.blit(self.background, (0, 0))
            self.background.blit(logo, logo.get_rect(center=bg_center))
            pygame.display.flip()

if __name__ == '__main__':
    game = SpaceInvader().run()
