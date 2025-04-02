import pygame as pg
import math


class Entity(pg.sprite.Sprite):
    def __init__(self, pos: list[int], image: pg.Surface) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(0, 0)

    def update(self, screensize: list[int], speed: int) -> None:
        self.position += self.velocity
        self.rect.center = self.position.xy
        self.rect.clamp_ip(pg.Rect((0, 0), screensize))

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.image, self.rect)


class Player(Entity):
    def __init__(self, pos: list[int], image: pg.Surface) -> None:
        super().__init__(pos, image)
        self.ammo = 50

    def update(self, screensize: list[int], speed: int) -> None:
        self.velocity = pg.Vector2(0, 0)
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.velocity.x = -speed
        if keys[pg.K_d]:
            self.velocity.x = speed
        if keys[pg.K_w]:
            self.velocity.y = -speed
        if keys[pg.K_s]:
            self.velocity.y = speed

        super().update(screensize, speed)


class Enemy(Entity):
    def __init__(
        self, pos: list[int], image: pg.Surface, speed: int, angle: int
    ) -> None:
        super().__init__(pos, image)
        self.speed = speed
        self.angle = angle
        self.velocity = pg.Vector2(
            math.cos(math.radians(self.angle)) * self.speed,
            math.sin(math.radians(self.angle)) * self.speed,
        )

    def update(
        self, screensize: list[int], target: pg.sprite.Sprite, act_dist: int
    ) -> None:
        super().update(screensize, self.speed)
        dist = math.sqrt(((target.position.x - self.position.x) ** 2) + ((target.position.y - self.position.y) ** 2))
        if dist > act_dist:
            print(dist)
            self.position += self.velocity
            self.rect.center = self.position

            self.rect.clamp_ip(pg.Rect((0, 0), screensize))

    def draw(self, screen):
        super().draw(screen)

    def collision(self, collide_rect: pg.Rect) -> bool:
        return self.rect.colliderect(collide_rect)
