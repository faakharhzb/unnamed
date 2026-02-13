import pygame as pg
from pygame.sprite import Sprite
import math


class Bullet(Sprite):
    def __init__(
        self,
        image: pg.Surface,
        size: tuple[int, int],
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

    def update(self, screen: pg.Surface, dt: float):
        self.speed = self.base_speed * dt
        self.velocity = pg.Vector2(self.speed, 0).rotate(self.angle)
        self.position += self.velocity
        self.rect.centerx, self.rect.centery = self.position.x, self.position.y

        if not screen.get_rect().contains(self.rect):
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
    # TODO: fix gun jittering
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

        angle = int(math.degrees(math.atan2(y, x)))
        angle = (angle + 360) % 360
        return angle

    def update(self, pos: pg.Vector2) -> None:
        self.angle = self.get_angle(pos)
        self.position = pos
        self.rect.center = self.position.x, self.position.y

        if self.angle in self.cache:
            self.image = self.cache[self.angle][0]
            self.rect = self.cache[self.angle][1]
        else:
            self.image = pg.transform.rotate(
                self.base_image,
                -self.angle,
            )

            self.rect = self.image.get_rect(center=self.position)
            self.cache[self.angle] = [self.image, self.rect.copy()]

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(
            self.image,
            self.rect,
        )
