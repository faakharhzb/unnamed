import pygame as pg
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, size: list[int], pos: list[int], color: pg.Color) -> None:
        super().__init__()

        self.size = size
        self.pos = pos
        self.image = pg.Surface(self.size)
        self.rect = self.image.get_rect(center=self.pos)