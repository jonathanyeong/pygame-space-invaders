import pygame

def load_image(name):
    image = pygame.image.load(name)
    return pygame.transform.scale(image, (27, 20))
