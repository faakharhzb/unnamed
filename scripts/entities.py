import math
from numpy import ndarray
import pygame as pg
from pathfinding.core.grid import Grid, GridNode
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.finder.a_star import AStarFinder


class Entity(pg.sprite.Sprite):
    def __init__(self, pos: list[int], image: pg.Surface, speed: int) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.velocity = [0, 0]

        self.base_speed = speed

    def clamp(self, w: int, h: int) -> None:
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > h:
            self.rect.bottom = h
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > w:
            self.rect.right = w

    def update(self, dt: float) -> None:
        self.speed = self.base_speed * dt

        self.velocity = [i * self.speed for i in self.velocity]

        self.rect.centerx = self.velocity[0]
        self.rect.centery = self.velocity[1]

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.image, self.rect)


class Player(Entity):
    def __init__(self, pos: list[int], image: pg.Surface, base_speed: int) -> None:
        super().__init__(pos, image, base_speed)
        self.ammo = 30
        self.moved = False

    def clamp(self, w: int, h: int) -> None:
        super().clamp(w, h)

    def update(self, dt: float, w: int, h: int) -> None:
        super().update(dt)

        up, down, left, right = False, False, False, False

        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.velocity[0] = -self.speed
            left = True
        if keys[pg.K_d]:
            self.velocity[0] = self.speed
            right = True
        if keys[pg.K_w]:
            self.velocity[1] = -self.speed
            up = True
        if keys[pg.K_s]:
            self.velocity[1] = self.speed
            down = True

        self.clamp(w, h)

        self.moved = up or down or left or right

        self.velocity = [0, 0]

    def draw(self, screen: pg.Surface):
        super().draw(screen)


class Enemy(Entity):
    def __init__(
        self,
        pos: list[int],
        image: pg.Surface,
        base_speed: int,
        matrix: list | ndarray,
        rows: int,
        cols: int,
    ) -> None:
        super().__init__(pos, image, base_speed)

        self.rows = rows
        self.cols = cols

        self.base_speed = base_speed
        self.velocity = [self.base_speed, 0]
        self.matrix = matrix

        self.grid = Grid(matrix=self.matrix)
        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

        self.path = []
        self.player_moved = False
        self.arrived = 0

    def find_path(self, target_pos: list) -> list[GridNode]:
        self.arrived = 0
        print(
            int(self.rect.centerx // 40),
            int(self.rect.centery // 40),
        )

        self.start = self.grid.node(
            int(self.rect.centerx // 40),
            int(self.rect.centery // 40),
        )

        self.end = self.grid.node(
            int(target_pos[0] // 40),
            int(target_pos[1] // 40),
        )

        path, _ = self.finder.find_path(self.start, self.end, self.grid)
        return path

    def get_angle(self, target_pos: pg.Vector2) -> int:
        angle = math.degrees(
            math.atan2(
                self.target_pos[1] - self.rect.centery,
                self.target_pos[0] - self.rect.centerx,
            )
        )
        return int(angle)

    def clamp(self, w: int, h: int) -> None:
        super().clamp(w, h)

    def update(
        self, target: pg.sprite.Sprite, act_dist: int, dt: float, w: int, h: int
    ) -> None:
        self.speed = self.base_speed * dt

        if not self.path or self.player_moved:
            self.path = self.find_path(target.rect.center)

        if self.path:
            point = self.path[0]
            tile_size = 40
            self.target_pos = [
                point.x * tile_size + tile_size // 2,
                point.y * tile_size + tile_size // 2,
            ]

            angle = self.get_angle(self.target_pos)
            rad = math.radians(angle)
            self.velocity = [math.cos(rad) * self.speed, math.sin(rad) * self.speed]

            if self.rect.collidepoint(self.target_pos):
                self.path.pop(0)
                self.arrived += 1

        self.rect.centerx += self.velocity[0]
        self.rect.centery += self.velocity[1]

        self.velocity = [0, 0]

        self.clamp(w, h)

    def draw(self, screen):
        super().draw(screen)

    def collision(self, collide_rect: pg.Rect) -> bool:
        return self.rect.colliderect(collide_rect)
