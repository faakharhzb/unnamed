import math
import random
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
        self.velocity = pg.Vector2()
        self.base_speed = speed
        self.speed = speed

    def update(self, dt: float) -> None:
        self.speed = self.base_speed * dt
        self.position += self.velocity * self.speed
        self.rect.center = self.position

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.image, self.rect)

    def clamp(
        self, pos: pg.Vector2, min_pos: pg.Vector2, max_pos: pg.Vector2
    ) -> pg.Vector2:
        return pg.Vector2(
            max(min_pos.x + self.image.get_width() // 2, min(pos.x, max_pos.x)),
            max(min_pos.y + self.image.get_height() // 2, min(pos.y, max_pos.y)),
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
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.velocity.x = -1
            left = True
        elif keys[pg.K_d]:
            self.velocity.x = 1
            right = True
        else:
            self.velocity.x = 0

        if keys[pg.K_w]:
            self.velocity.y = -1
            up = True
        elif keys[pg.K_s]:
            self.velocity.y = 1
            down = True
        else:
            self.velocity.y = 0

        super().clamp(self.position, pg.Vector2(0, 0), pg.Vector2(w, h))
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
        tile_x: int,
        tile_y: int,
        rows: int,
        cols: int,
    ) -> None:
        super().__init__(pos, image, base_speed)
        self.rows = rows
        self.cols = cols
        self.matrix = matrix
        self.tile_x, self.tile_y = tile_x, tile_y

        self.grid = Grid(matrix=self.matrix)
        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

        self.arrived = []
        self.path = [[], ""]
        self.target_pos = pg.Vector2()

    def find_path(self, target_pos: pg.Vector2, reason: str) -> list[GridNode, str]:
        self.start = self.grid.node(
            min(int(self.position.x // self.tile_x), self.rows - 1),
            min(int(self.position.y // self.tile_y), self.cols - 1),
        )
        self.end = self.grid.node(
            min(int(target_pos.x // self.tile_x), self.rows - 1),
            min(int(target_pos.y // self.tile_y), self.cols - 1),
        )
        path, _ = self.finder.find_path(self.start, self.end, self.grid)
        return [path, reason]

    def get_angle(self, target_pos: pg.Vector2) -> float:
        return math.degrees(
            math.atan2(
                target_pos.y - self.position.y,
                target_pos.x - self.position.x,
            )
        )

    def update(
        self, dt: float, w: int, h: int, target: Entity, chase_distance: int
    ) -> None:
        super().update(dt)
        self.position = super().clamp(self.position, pg.Vector2(), pg.Vector2(w, h))

        if not self.path:
            self.path = self.find_path(target.position, "roam")

        distance = self.position.distance_to(target.position)
        if distance < chase_distance:
            if target.moved or self.path[1] != "chase" or len(self.path[0]) == 0:
                self.path = self.find_path(target.position, "chase")
        else:
            if self.path[1] != "roam" or len(self.path[0]) == 0:
                roam_dest = pg.Vector2(
                    random.randint(0, self.rows) * self.tile_x,
                    random.randint(0, self.cols) * self.tile_y,
                )
                self.path = self.find_path(roam_dest, "roam")

        if self.path[0]:
            point = self.path[0][0]
            self.target_pos = pg.Vector2(point.x * self.tile_x, point.y * self.tile_y)
            angle = self.get_angle(self.target_pos)

            if self.path[1] == "chase":
                self.velocity = pg.Vector2(self.speed, 0).rotate(angle)
            else:
                self.velocity = pg.Vector2(self.speed - 0.5, 0).rotate(angle)

            if self.rect.collidepoint(self.target_pos):
                self.path[0].pop(0)

        self.rect.center = self.position

    def draw(self, screen):
        super().draw(screen)

    def collision(self, collide_rect: pg.Rect) -> bool:
        return self.rect.colliderect(collide_rect)
