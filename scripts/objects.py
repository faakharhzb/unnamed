import pygame as pg
from pygame.sprite import Sprite
import math
from .utilities import cache_angles


class Bullet(Sprite):
    def __init__(
        self,
        size: tuple[int, int],
        pos: tuple[float, float],
        angle: float,
        base_speed: float,
        colour: pg.Color,
    ):
        super().__init__()
        self.image = pg.Surface(size)
        self.image.fill(colour)

        self.rect = self.image.get_rect(center=pos)

        self.base_speed = base_speed
        self.position = pg.Vector2(pos)
        self.angle = angle
        self.velocity = pg.Vector2(
            math.cos(math.radians(self.angle)) * base_speed,
            math.sin(math.radians(self.angle)) * base_speed,
        )

    def update(self, screen: pg.Surface, dt: float):
        self.velocity = pg.Vector2(
            math.cos(math.radians(self.angle)) * (self.base_speed * dt),
            math.sin(math.radians(self.angle)) * (self.base_speed * dt),
        )
        self.position += self.velocity
        self.rect.centerx, self.rect.centery = self.position.x, self.position.y

        if not screen.get_rect().contains(self.rect):
            self.kill()

    def hit(self, collide_rect: pg.Rect) -> None:
        return self.rect.colliderect(collide_rect)

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.image, self.position)


class Obtainable_Item(Sprite):
    def __init__(self, image: pg.Surface, pos: tuple[float, float]):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.position = pg.Vector2(pos)

    def collision(self, collide_object: pg.Rect):
        return self.rect.colliderect(collide_object)

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.image, self.position)


class Gun(Sprite):
    def __init__(self, image: pg.Surface, pos: list[int, int]) -> None:
        super().__init__()
        self.base_image = image
        self.image = self.base_image.copy()

        self.position = pg.Vector2(pos)
        self.rect = self.image.get_rect(center=pos)

        self.cache = {}

    def update(self, angle: int, pos: list[int, int]) -> None:
        self.cache = cache_angles(self.base_image)

        self.angle = -angle
        self.position = pg.Vector2(pos)
        self.rect.center = self.position.x, self.position.y

        if angle > 90 or angle < -90:
            self.image = (
                pg.transform.flip(self.cache[int(self.angle)], False, True),
                -self.angle,
            )

        else:
            self.image = (
                pg.transform.flip(self.cache[int(self.angle)], False, False),
                -self.angle,
            )

        self.rect = self.cache[int(self.angle)].get_rect(center=self.rect.center)

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(
            self.cache[int(self.angle)],
            self.rect,
        )
