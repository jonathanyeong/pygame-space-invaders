import pygame
class Video (object):
    def set_display(self, width, height, isFullScreen):
        screen = None
        if (isFullScreen is False):
            screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
        else:
            screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.FULLSCREEN)

        pygame.display.set_caption("Pygame Space Invader Clone")
        screen.fill((0,0,0))
        pygame.display.flip()
        return screen
