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
        speed: float,
        colour: pg.Color,
    ):
        super().__init__()
        self.image = pg.Surface(size)
        self.image.fill(colour)

        self.rect = self.image.get_rect(center=pos)

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
            self.image = pg.transform.rotate(
                pg.transform.flip(self.cache[int(self.angle)], False, True), -self.angle
            )

        else:
            self.image = pg.transform.rotate(
                pg.transform.flip(self.cache[int(self.angle)], False, False), -self.angle
            )

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(
            self.cache[int(self.angle)],
            (
                self.rect # - (self.image.get_width() // 2),
                
                # self.position.y  - (self.image.get_height() // 2),
            ),
        )
