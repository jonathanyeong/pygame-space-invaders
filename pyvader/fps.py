import pygame

class Fps(object):
    def __init__(self):
        self.fps = 60
        self.clock = pygame.time.Clock()
    
    def tick(self):
        return self.clock.tick(self.fps)
