import pygame as pg

class Entity(pg.sprite.Sprite):
    def __init__(self, pos: list[int], image: pg.Surface) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)

        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(0, 0)
        self.acceleration = pg.Vector2(0, 0)

        self.accel_value = 0
        self.friction = 0.12

        self.wall_offset = [15, 15]

    def update(self, screensize: list[int]) -> None:
        self.acceleration = pg.Vector2(0, 0)

        if self.position.x < 0:
            self.position.x = 0 + self.wall_offset[0]
            self.velocity.x = 0
        if self.position.x > screensize[0]:
            self.position.x = screensize[0] - self.wall_offset[0]
            self.velocity.x = 0
        if self.position.y < 0:
            self.position.y = 0 + self.wall_offset[0]
            self.velocity.y = 0
        if self.position.y > screensize[1]:
            self.position.y = screensize[1] - self.wall_offset[0]
            self.velocity.y = 0

        self.rect.center = self.position

    def render(self, screen: pg.Surface) -> None:
        screen.blit(self.image, self.rect)


class Player(Entity):
    def __init__(self, pos: list[int], image: pg.Surface) -> None:
        super().__init__(pos, image)
        self.accel_value = 0.5

    def update(self, screensize: list[int], dt: float) -> None:
        super().update(screensize)

        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.acceleration.x = -self.accel_value * dt
        if keys[pg.K_d]:
            self.acceleration.x = self.accel_value * dt
        if keys[pg.K_w]:
            self.acceleration.y = -self.accel_value * dt
        if keys[pg.K_s]:
            self.acceleration.y = self.accel_value * dt

        self.acceleration.x -= self.velocity.x * self.friction
        self.acceleration.y -= self.velocity.y * self.friction

        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

    def render(self, screen: pg.Surface) -> None:
        super().render(screen)
