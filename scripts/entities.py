import pygame as pg


class Entity(pg.sprite.Sprite):
    def __init__(self, pos: list[int], image: pg.Surface) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(0, 0)

    def update(self, screensize: list[int], speed: int) -> None:
        self.position += self.velocity
        self.rect.centerx, self.rect.centery = self.position.x, self.position.y

        self.key = pg.key.get_pressed()

        self.rect.clamp_ip(pg.Rect((0, 0), screensize))

        if self.velocity.length() != 0:
            self.velocity = self.velocity.normalize() * speed

        self.velocity = pg.Vector2(0, 0)

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.image, self.rect)


class Player(Entity):
    def __init__(self, pos: list[int], image: pg.Surface) -> None:
        super().__init__(pos, image)
        self.ammo = 50

    def update(self, screensize: list[int], speed: int) -> None:
        super().update(screensize, speed)

        if self.key[pg.K_a]:
            self.velocity.x = -speed
        if self.key[pg.K_d]:
            self.velocity.x = speed
        if self.key[pg.K_w]:
            self.velocity.y = -speed
        if self.key[pg.K_s]:
            self.velocity.y = speed

    def draw(self, screen):
        super().draw(screen)
