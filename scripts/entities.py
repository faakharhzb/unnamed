import pygame as pg


class Entity(pg.sprite.Sprite):
    def __init__(self, pos: list[int], image: pg.Surface, speed: int) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(0, 0)

        self.base_speed = speed

    def update(self) -> None:
        self.position += self.velocity
        self.rect.center = self.position.x, self.position.y

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.image, self.rect)


class Player(Entity):
    def __init__(self, pos: list[int], image: pg.Surface, base_speed: int) -> None:
        super().__init__(pos, image, base_speed)
        self.ammo = 50

    def update(self, dt: float) -> None:
        speed = self.base_speed * dt
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

        super().update()

    def draw(self, screen: pg.Surface):
        super().draw(screen)


class Enemy(Entity):
    def __init__(
        self,
        pos: list[int],
        image: pg.Surface,
        base_speed: int,
        angle: int,
    ) -> None:
        super().__init__(pos, image, base_speed)

        self.base_speed = base_speed
        self.velocity = pg.Vector2(self.base_speed, 0).rotate(angle)

    def update(
        self, target: pg.sprite.Sprite, act_dist: int, angle: float, dt: float
    ) -> None:
        speed = self.base_speed * dt
        self.angle = angle
        dist = self.position.distance_to(target.position)
        if dist < act_dist:
            self.velocity = pg.Vector2(speed, 0).rotate(angle)

        else:
            self.velocity = pg.Vector2(0, 0)

        super().update()

    def draw(self, screen):
        super().draw(screen)

    def collision(self, collide_rect: pg.Rect) -> bool:
        return self.rect.colliderect(collide_rect)
