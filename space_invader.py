#!/usr/bin/python

import os, sys
import pygame
from pygame.locals import *

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((600, 480))
    pygame.display.set_caption("PyGame Space Invaders clone")

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((10, 10, 10))

    font = pygame.font.Font(None, 42) # Init some font object
    # Display title text
    title_text = font.render("Space Invaders", 1, (250, 250, 250))
    textpos = title_text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(title_text, textpos)
    # Display instruction text
    instruction_text = font.render("Press B to start", 1, (250, 250, 250))
    instruction_textpos = instruction_text.get_rect()
    instruction_textpos.midbottom = background.get_rect().midbottom
    background.blit(instruction_text, instruction_textpos)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        screen.blit(background, (0, 0))
        pygame.display.flip()

if __name__ == '__main__':
    main()
