import pygame


class Fps(object):
    def __init__(self):
        self.fps = 120
        self.clock = pygame.time.Clock()

    def tick(self):
        return self.clock.tick(self.fps)
