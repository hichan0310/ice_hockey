import pygame

from settings import *


class Brick(pygame.sprite.Sprite):
    def __init__(self, pos, size, group, color, sabunmyon):
        super().__init__(group)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.sabunmyon=sabunmyon

