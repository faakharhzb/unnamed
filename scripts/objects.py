import pygame as pg
from pygame.sprite import Sprite
import math


class Bullet(Sprite):
    def __init__(
        self,
        image: pg.Surface,
        pos: tuple[float, float],
        angle: float,
        base_speed: float,
    ):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)

        self.base_speed = base_speed
        self.position = pg.Vector2(pos)
        self.angle = angle
        self.velocity = pg.Vector2()

        self.image = pg.transform.rotate(self.image, -self.angle)

    def update(self, screen_rect: pg.Rect, dt: float):
        self.speed = self.base_speed * dt
        self.velocity = pg.Vector2(self.speed, 0).rotate(self.angle)
        self.position += self.velocity
        self.rect.centerx, self.rect.centery = self.position.x, self.position.y

        if not screen_rect.contains(self.rect):
            self.kill()

    def hit(self, collide_rect: pg.Rect) -> None:
        return self.rect.colliderect(collide_rect)

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.image, self.rect)


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
        self.angle = 0

    def get_angle(self, pos: pg.Vector2) -> None:
        mousepos = pg.mouse.get_pos()
        x = mousepos[0] - pos.x
        y = mousepos[1] - pos.y

        angle = round(math.degrees(math.atan2(y, x)))
        angle = (angle + 360) % 360
        return angle

    def update(self, pos: pg.Vector2) -> None:
        self.angle = self.get_angle(pos)
        rounded_angle = round(self.angle / 3) * 3

        if self.angle in self.cache:
            self.image = self.cache[rounded_angle]
        else:
            if 90 <= self.angle <= 270:
                self.image = pg.transform.flip(self.base_image, False, True)
            else:
                self.image = self.base_image.copy()

            self.image = pg.transform.rotate(
                self.image,
                -rounded_angle,
            )

            self.cache[rounded_angle] = self.image

        self.rect.center = pos.xy
        self.rect.size = self.image.get_size()

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(
            self.image,
            self.rect,
        )
