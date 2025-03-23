import pygame as pg
from pygame.sprite import Sprite
import math

class Bullet(Sprite): 
    def __init__(self, size: tuple[int, int], pos: tuple[float, float], angle: float, speed: float, colour: pg.Color): 
        super().__init__()
        self.image = pg.Surface(size)
        self.image.fill(colour)

        self.rect = image.get_rect(center = pos)

        self.speed = speed
        self.position = pg.Vector2(pos)
        self.angle = angle
        self.velocity = pg.Vector2(math.cos(math.radians(self.angle)) * speed,
                                math.sin(math.radians(self.angle)) * speed)

    def update(self, screen: pg.Surface): 

        self.position += self.velocity
        self.rect.centerx, self.rect.centery = self.position.x, self.position.y

        if not screen.get_rect().contains(self.rect):
            self.kill()


class Obtainable_Item(Sprite):
    def __init__(self, image: pg.Surface, pos: tuple[float, float]):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.position = pg.Vector2(pos)

    def collision(self, collide_object: pg.Rect):
        return self.rect.colliderect(collide_object)