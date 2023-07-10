from math import atan, sin, cos, sqrt, pi
import pygame

from settings import *


class Ball(pygame.sprite.Sprite):
    def __init__(self, pos, brick_group, player_group):
        super().__init__()
        self.image = pygame.Surface(BALL_SIZE).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, (160, 219, 115), (BALL_RADIUS,) * 2, BALL_RADIUS)
        self.rect = self.image.get_rect(center=pos)
        self.brick_group = brick_group
        self.player_group = player_group
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 9
        self.vector = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(*pos)

    def brick_collide(self):
        for brick in self.brick_group.sprites():
            offset = brick.rect.x - self.rect.x, brick.rect.y - self.rect.y
            if self.mask.overlap_area(brick.mask, offset) <= 0:
                continue

            if brick.rect.bottom >= self.rect.centery >= brick.rect.top or \
                    self.vector.y > 0 and self.rect.centery > brick.rect.bottom or \
                    self.vector.y < 0 and self.rect.centery < brick.rect.top:
                self.vector.x = (1 if brick.sabunmyon == 1 or brick.sabunmyon == 4 else -1) * abs(self.vector.x)
            elif brick.rect.left <= self.rect.centerx <= brick.rect.right or \
                    self.vector.x > 0 and self.rect.centerx > brick.rect.right or \
                    self.vector.x < 0 and self.rect.centerx < brick.rect.left:
                self.vector.y = (-1 if brick.sabunmyon == 1 or brick.sabunmyon == 2 else 1) * abs(self.vector.y)
            else:
                self.vector.x = (1 if brick.sabunmyon == 1 or brick.sabunmyon == 4 else -1) * abs(self.vector.x)
                self.vector.y = (1 if brick.sabunmyon == 1 or brick.sabunmyon == 2 else -1) * abs(self.vector.y)

    def player_collide(self):
        M, m = PLAYER_MASS, BALL_MASS
        for player in self.player_group.sprites():
            player_location = pygame.math.Vector2(player.x, player.y)
            ball_location = pygame.math.Vector2(self.pos.x, self.pos.y)
            player_speed = pygame.math.Vector2(*player.v)
            ball_speed = self.vector
            a = player_location - ball_location
            b = player_speed - ball_speed
            if a.x**2+a.y**2 < (BALL_RADIUS + PLAYER_RADIUS) ** 2 and a.x * b.x + a.y * b.y < 0:
                try:
                    theta1 = atan((player_location.y - ball_location.y) / (player_location.x - ball_location.x))
                except:
                    try:
                        theta1 = pi / 2 * abs(player_location.y - ball_location.y) / (player_location.y - ball_location.y)
                    except:
                        theta1 = 0
                try:
                    theta2 = atan((player_speed.y - ball_speed.y) / (player_speed.x - ball_speed.x))
                except:
                    try:
                        theta2 = pi / 2 * abs(player_speed.y - ball_speed.y) / (player_speed.y - ball_speed.y)
                    except:
                        theta2 = 0
                result = 2 * theta1 - theta2
                v_sang = sqrt((player_speed[1] - ball_speed[1]) ** 2 + (player_speed[0] - ball_speed[0]) ** 2) / 2
                temp = pygame.math.Vector2(v_sang * cos(result), v_sang * sin(result))
                self.vector = (temp * M + M * player_speed + m * ball_speed) / (M + m)

        # offset = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        # if self.mask.overlap_area(player.mask, offset) > 0:
        #     if player.rect.collidepoint(self.rect.center) or self.rect.centery > player.rect.bottom:
        #         self.rect.top = player.rect.bottom
        #         self.vector = pygame.math.Vector2(0, 10)
        #     elif player.rect.bottom > self.rect.centery > player.rect.top:
        #         self.vector.x *= -1
        #     else:
        #         temp = player.rect.centerx - self.rect.centerx
        #         temp = abs(temp ** 0.7) * (1 if temp > 0 else -1)
        #         angle = -90 - temp * 2
        #         self.vector.x = math.cos(math.radians(angle))
        #         self.vector.y = math.sin(math.radians(angle))
        #         self.vector *= self.speed

    def update(self):
        self.pos += self.vector
        if sqrt(self.vector.x ** 2 + self.vector.y ** 2) > 5:
            gasokdo = 0.1
            self.vector -= pygame.math.Vector2(gasokdo * self.vector.x / sqrt(self.vector.x ** 2 + self.vector.y ** 2),
                                               gasokdo * self.vector.y / sqrt(self.vector.x ** 2 + self.vector.y ** 2))
        self.rect.center = round(self.pos.x), round(self.pos.y)
        if self.rect.top < 60:
            self.rect.top = -self.rect.top + 120
            self.vector.y *= -1
        if self.rect.bottom > SCREEN_HEIGHT - 60:
            self.rect.bottom = -self.rect.bottom + 2 * (SCREEN_HEIGHT - 60)
            self.vector.y *= -1
        if self.rect.right < 0:
            self.pos = pygame.math.Vector2(SCREEN_WIDTH / 4 * 3, SCREEN_HEIGHT / 2)
            self.vector = pygame.math.Vector2(0, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.pos = pygame.math.Vector2(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2)
            self.vector = pygame.math.Vector2(0, 0)

        self.brick_collide()
        self.player_collide()
