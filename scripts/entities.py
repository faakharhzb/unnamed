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

    def clamp(
        self, pos: pg.Vector2, min_pos: pg.Vector2, max_pos: pg.Vector2
    ) -> pg.Vector2:
        return pg.Vector2(
            max(min_pos.x, min(pos.x, max_pos.x)), max(min_pos.y, min(pos.y, max_pos.y))
        )


class Player(Entity):
    def __init__(self, pos: list[int], image: pg.Surface, base_speed: int) -> None:
        super().__init__(pos, image, base_speed)
        self.ammo = 30
        self.moved = False

    def update(self, dt: float, w: int, h: int) -> None:
        super().update(dt)
        self.position = super().clamp(self.position, pg.Vector2(0, 0), pg.Vector2(w, h))

        up, down, left, right = False, False, False, False

        self.velocity = pg.Vector2(0, 0)
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.velocity.x = -self.speed
            left = True
        if keys[pg.K_d]:
            self.velocity.x = self.speed
            right = True
        if keys[pg.K_w]:
            self.velocity.y = -self.speed
            up = True
        if keys[pg.K_s]:
            self.velocity.y = self.speed
            down = True

        self.moved = up or down or left or right

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
        self.path = self.find_path(pg.Vector2())

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
                self.target_pos.y - self.position.y,
                self.target_pos.x - self.position.x,
            )
        )

        return angle

    def update(
        self, target: pg.sprite.Sprite, act_dist: int, dt: float, w: int, h: int
    ) -> None:
        super().update(dt)
        self.position = super().clamp(self.position, pg.Vector2(0, 0), pg.Vector2(w, h))

        if target.moved:
            self.path = self.find_path(pg.Vector2(target.rect.center))

        for point in self.path:
            if point not in self.arrived:
                tile_size = 40
                self.target_pos = pg.Vector2(point.x * tile_size, point.y * tile_size)
                direction = self.target_pos - self.position

                if direction.length() > 0:
                    direction = direction.normalize()
                    self.velocity = direction * self.speed
                else:
                    self.velocity = pg.Vector2(0, 0)

                # Mark point as arrived when close enough
                if (self.target_pos - self.position).length() < 5:
                    self.arrived.append(point)

                break

    def draw(self, screen):
        super().draw(screen)

    def collision(self, collide_rect: pg.Rect) -> bool:
        return self.rect.colliderect(collide_rect)
