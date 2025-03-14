import pygame as pg

class Entity(pg.sprite.Sprite):
    def __init__(self, pos: list[int], image: pg.Surface) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_frect(center=pos)
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(0, 0)

    def update(self, screensize: list[int], speed: int, dt:float) -> None:
        self.position += self.velocity
        self.rect.centerx, self.rect.centery = self.position.x, self.position.y

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screensize[0]:
            self.rect.right = screensize[0]
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screensize[1]:
            self.rect.bottom = screensize[1]

        if self.velocity.length() != 0:
            self.velocity = self.velocity.normalize() * speed * dt

class Player(Entity):
    def __init__(self, pos: list[int], image: pg.Surface) -> None:
        super().__init__(pos, image)

    def update(self, screensize: list[int], dt: float, speed: int) -> None:
        keys = pg.key.get_pressed()
        self.velocity = pg.Vector2(0, 0)

        if keys[pg.K_a]:
            self.velocity.x = -speed
        if keys[pg.K_d]:
            self.velocity.x = speed
        if keys[pg.K_w]:
            self.velocity.y = -speed
        if keys[pg.K_s]:
            self.velocity.y = speed
        
        super().update(screensize, speed, dt)