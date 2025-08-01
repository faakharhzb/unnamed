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
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(0, 0)

        self.base_speed = speed

    def update(self, dt: float) -> None:
        self.speed = self.base_speed * dt

        if self.velocity.length() != 0:
            self.velocity = self.velocity.normalize() * self.speed

        self.position += self.velocity
        self.rect.center = self.position.xy

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.image, self.rect)


class Player(Entity):
    def __init__(self, pos: list[int], image: pg.Surface, base_speed: int) -> None:
        super().__init__(pos, image, base_speed)
        self.ammo = 30

    def update(self, dt: float) -> None:
        super().update(dt)

        self.velocity = pg.Vector2(0, 0)
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.velocity.x = -self.speed
        if keys[pg.K_d]:
            self.velocity.x = self.speed
        if keys[pg.K_w]:
            self.velocity.y = -self.speed
        if keys[pg.K_s]:
            self.velocity.y = self.speed

    def draw(self, screen: pg.Surface):
        super().draw(screen)


class Enemy(Entity):
    def __init__(
        self,
        pos: list[int],
        image: pg.Surface,
        base_speed: int,
        matrix: list | ndarray,
    ) -> None:
        super().__init__(pos, image, base_speed)

        self.base_speed = base_speed
        self.velocity = pg.Vector2(self.base_speed, 0)
        self.matrix = matrix

        self.grid = Grid(matrix=self.matrix)
        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

        self.arrived = []

    def find_path(self, target_pos: pg.Vector2) -> list[GridNode]:
        self.start = self.grid.node(
            int(self.position.x // len(self.matrix[0])),
            int(self.position.y // len(self.matrix[1])),
        )

        self.end = self.grid.node(
            int(target_pos.x // len(self.matrix[0])),
            int(target_pos.y // len(self.matrix[1])),
        )

        path, _ = self.finder.find_path(self.start, self.end, self.grid)
        return path

    def get_angle(self, target_pos: pg.Vector2) -> int:
        angle = math.degrees(
            math.atan2(
                self.target_pos.y - self.position.y, self.target_pos.x - self.position.x
            )
        )
        return angle

    def update(self, target: pg.sprite.Sprite, act_dist: int, dt: float) -> None:
        super().update(dt)

        self.path = self.find_path(target.position)

        for point in self.path:
            if point not in self.arrived:
                self.target_pos = pg.Vector2(
                    point.x * len(self.matrix[0]), point.y * len(self.matrix[1])
                )
                self.angle = self.get_angle(self.target_pos)

                if len(self.path) - len(self.arrived) < 15:
                    self.velocity = pg.Vector2(self.speed).rotate(self.angle)
                else:
                    self.velocity = pg.Vector2(0, 0)
            else:
                self.arrived.append(point)

    def draw(self, screen):
        super().draw(screen)

    def collision(self, collide_rect: pg.Rect) -> bool:
        return self.rect.center == collide_rect.center
