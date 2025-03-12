import pygame as pg

class Entity(pg.sprite.Sprite):
    def __init__(self, pos: list[int], image: pg.Surface) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)

        self.position = pg.Vector2(pos)

    def update(self, screensize: list[int]) -> None:

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screensize[0]:
            self.rect = screensize[0]
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screensize[1]:
            self.rect.bottom = screensize[1]
            

class Player(Entity):
    def __init__(self, pos: list[int], image: pg.Surface) -> None:
        super().__init__(pos, image)

    def update(self, screensize: list[int], dt: float, speed: int) -> None:
        super().update(screensize)

        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.rect.x -= speed * dt
        if keys[pg.K_d]:
            self.rect.x += speed * dt
        if keys[pg.K_w]:
            self.rect.y -= speed * dt
        if keys[pg.K_s]:
            self.rect.y += speed * dt