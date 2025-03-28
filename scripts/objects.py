import pygame as pg
from pygame.sprite import Sprite
import math


class Bullet(Sprite):
    def __init__(
        self,
        size: tuple[int, int],
        pos: tuple[float, float],
        angle: float,
        speed: float,
        colour: pg.Color,
    ):
        super().__init__()
        self.image = pg.Surface(size)
        self.colour = colour
        self.image.fill(self.colour)

        self.rect = pg.Rect((pos[0] - size[0] / 2, pos[1] - size[1] / 2), size)

        self.speed = speed
        self.position = pg.Vector2(pos)
        self.angle = angle
        self.velocity = pg.Vector2(
            math.cos(math.radians(self.angle)) * speed,
            math.sin(math.radians(self.angle)) * speed,
        )

    def update(self, screen: pg.Surface):
        self.position += self.velocity
        self.rect.centerx, self.rect.centery = self.position.x, self.position.y

        if not screen.get_rect().contains(self.rect):
            self.kill()


class Obtainable_Item(Sprite):
    def __init__(self, image: pg.Surface, pos: tuple[float, float]):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.position = pg.Vector2(pos)

    def collision(self, collide_object: pg.Rect):
        return self.rect.colliderect(collide_object)


class Gun(Sprite):
    def __init__(self, image: pg.Surface, pos: list[int, int]):
        super().__init__()
        self.base_image = image
        self.image = self.base_image.copy()

        self.position = pg.Vector2(pos)
        self.rect = self.image.get_rect(center=pos)

    def update(self, angle: int, pos: list[int, int]):
        self.position = pg.Vector2(pos)
        self.rect.centerx, self.rect.centery = self.position.x, self.position.y
        self.image = pg.transform.rotate(self.base_image, -angle)
