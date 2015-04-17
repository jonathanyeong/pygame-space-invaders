#!/usr/bin/python

import os, sys
import pygame
from pygame.locals import *

class SpaceInvader(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 480))
        pygame.display.set_caption("PyGame Space Invaders clone")

        # Fill background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((10, 10, 10))

        self.font = pygame.font.Font(None, 42) # Init some font object

    def main(self):
        # Initialise screen
        # Display title text
        title_text = self.font.render("Space Invaders", 1, (250, 250, 250))
        textpos = title_text.get_rect()
        textpos.centerx = self.background.get_rect().centerx
        self.background.blit(title_text, textpos)
        # Display instruction text
        instruction_text = self.font.render("Press B to start", 1, (250, 250, 250))
        instruction_textpos = instruction_text.get_rect()
        instruction_textpos.midbottom = self.background.get_rect().midbottom
        self.background.blit(instruction_text, instruction_textpos)

        # Blit everything to the screen
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        # Event loop
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

            self.screen.blit(self.background, (0, 0))
            pygame.display.flip()

if __name__ == '__main__':
    game = SpaceInvader().main()
