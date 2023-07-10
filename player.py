import pygame

from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, camera, group):
        super().__init__(group)
        self.image = pygame.Surface(PLAYER_SIZE).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, (160, 219, 115), (PLAYER_RADIUS, PLAYER_RADIUS), PLAYER_RADIUS)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.9)))
        self.mask = pygame.mask.from_surface(self.image)
        self.camera = camera
        self.locationhistory = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.v = (0, 0)

    def update(self):
        try:
            self.x, self.y = self.camera.get_pos()
        except:
            pass
        self.locationhistory.pop()
        self.locationhistory = [(self.x, self.y)] + self.locationhistory
        self.rect.x = self.x - PLAYER_RADIUS
        self.rect.y = self.y - PLAYER_RADIUS
        self.v = ((self.locationhistory[0][0] - self.locationhistory[5][0]) / 5,
                  (self.locationhistory[0][1] - self.locationhistory[5][1]) / 5)
        # dx = pygame.mouse.get_pos()[0] - self.rect.centerx
        # dx = min(self.max_speed, max(-self.max_speed, dx))
        # self.rect.x += dx
