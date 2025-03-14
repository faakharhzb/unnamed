import pygame as pg
from pygame.sprite import Sprite
import math

class Bullet(Sprite):
    def __init__(self, size: list[int], pos: list[int], color: pg.Color, angle: math.degrees) -> None:
        super().__init__()
        self.size = size
        self.rect = pg.FRect(pos, self.size)
        self.position = pg.Vector2(pos)
        self.color = color
        self.angle = angle
        self.velocity = pg.Vector2(math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle)))

    def update(self, dt: float, speed: int) -> None:
        self.velocity = pg.Vector2(math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle)))

        self.velocity = speed * dt

        self.position += self.velocity
        self.rect.centerx, self.rect.centery = self.position.x, self.position.y





