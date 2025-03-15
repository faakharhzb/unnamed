from pygame.sprite import Sprite
from pygame.math import Vector2
from pygame import FRect, Surface, Color
import math

class Bullet(Sprite): 
    def __init__(self, size: tuple[int, int], pos: tuple[float, float], angle: float, speed: float, colour: Color): 
        super().__init__()
        self.image = Surface(size)
        self.colour = colour
        self.image.fill(self.colour)

        self.rect = FRect((pos[0] - size[0] / 2, pos[1] - size[1] / 2), size)

        self.speed = speed
        self.position = Vector2(pos)
        self.angle = angle
        self.velocity = Vector2(math.cos(math.radians(self.angle)),
                                math.sin(math.radians(self.angle)))

    def update(self, dt: float, screen: Surface): 
        self.velocity.x = self.speed * dt

        self.position += self.velocity
        self.rect.centerx, self.rect.centery = self.position.x, self.position.y

        if not screen.get_rect().contains(self.rect):
            self.kill()