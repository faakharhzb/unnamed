from itertools import cycle
import math
import random
import time
from numpy import ndarray
import pygame as pg

from pathfinding.core.grid import Grid, GridNode
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.finder.a_star import AStarFinder

from typing import Iterable
from .utilities import get_random_position


class Entity(pg.sprite.Sprite):
    def __init__(
        self,
        pos: list[int],
        image: pg.Surface | dict[str, list[pg.Surface]],
        speed: int,
        frame_delay: float = 0.2,
    ) -> None:
        super().__init__()

        self.animations: dict[str, cycle] = {}
        self.state = "idle"

        if isinstance(image, pg.Surface):
            self.image = image
            self.image_iter = None
        elif isinstance(image, dict):
            for state, frames in image.items():
                self.animations[state] = cycle(frames)

            self.state = next(cycle(image.keys()))
            self.image_iter = self.animations[self.state]
            self.image = next(self.image_iter)

        self.rect = self.image.get_rect(center=pos)
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2()

        self.base_speed = speed
        self.speed = speed

        self.frame_delay = frame_delay
        self.frame_timer = 0.0

    def set_state(self, state: str) -> None:
        if state in self.animations and state != self.state:
            self.state = state
            self.image_iter = self.animations[state]
            self.image = next(self.image_iter)
            self.frame_timer = 0.0

    def update(self, dt: float) -> None:
        self.speed = self.base_speed * dt
        if self.velocity.length() >= 1:
            self.velocity = self.velocity.normalize()

        self.position += self.velocity * self.speed
        self.rect.center = self.position

        if self.image_iter:
            self.frame_timer += dt / 60
            if self.frame_timer >= self.frame_delay:
                self.image = next(self.image_iter)
                self.frame_timer = 0.0

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.image, self.rect)

    def clamp(
        self, pos: pg.Vector2, min_pos: pg.Vector2, max_pos: pg.Vector2
    ) -> pg.Vector2:
        return pg.Vector2(
            max(
                min_pos.x + self.image.get_width() // 2,
                min(pos.x, max_pos.x - self.image.get_width() // 2),
            ),
            max(
                min_pos.y + self.image.get_height() // 2,
                min(pos.y, max_pos.y - self.image.get_height() // 2),
            ),
        )


class Player(Entity):
    def __init__(
        self,
        pos: list[int],
        image: pg.Surface | Iterable[pg.Surface],
        base_speed: int,
        matrix: list | ndarray,
        tile_x: int,
        tile_y: int,
        rows: int,
        cols: int,
        frame_delay: float = 0.2,
    ) -> None:
        super().__init__(pos, image, base_speed, frame_delay)
        self.ammo = 24
        self.moved = False
        self.kill_count = 0

        self.rows, self.cols = rows, cols
        self.matrix = matrix
        self.tile_x, self.tile_y = tile_x, tile_y

    def update(self, dt: float, bg_rect: pg.Rect) -> None:
        super().update(dt)

        up, down, left, right = False, False, False, False
        keys = pg.key.get_pressed()

        velocity = pg.Vector2()

        if keys[pg.K_a]:
            velocity.x = -1
            left = True
        if keys[pg.K_d]:
            velocity.x = 1
            right = True
        if keys[pg.K_w]:
            velocity.y = -1
            up = True
        if keys[pg.K_s]:
            velocity.y = 1
            down = True

        pos = self.position + velocity * self.speed

        col = int(pos.x // self.tile_x)
        row = int(pos.y // self.tile_y)

        if 0 <= row < self.rows and 0 <= col < self.cols:
            if self.matrix[row][col] == 0:
                velocity = pg.Vector2()
                pos = self.position

                (
                    up,
                    down,
                    left,
                    right,
                ) = False, False, False, False

        self.velocity = velocity
        self.position = super().clamp(
            self.position, pg.Vector2(bg_rect.topleft), pg.Vector2(bg_rect.bottomright)
        )
        self.moved = up or down or left or right

    def draw(self, screen: pg.Surface):
        super().draw(screen)


class Enemy(Entity):
    def __init__(
        self,
        pos: list[int],
        image: pg.Surface | Iterable[pg.Surface],
        base_speed: int,
        matrix: list | ndarray,
        tile_x: int,
        tile_y: int,
        rows: int,
        cols: int,
        frame_delay: float = 0.2,
        max_health: int = 4,
    ) -> None:
        super().__init__(pos, image, base_speed, frame_delay)

        self.rows, self.cols = rows, cols
        self.matrix = matrix
        self.tile_x, self.tile_y = tile_x, tile_y

        self.grid = Grid(matrix=self.matrix)
        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

        self.arrived = []
        self.path: list[list[GridNode, ...], str] = []
        self.target_pos = pg.Vector2()

        self.max_health = max_health
        self.health = self.max_health
        self.health_bar = pg.Rect(
            self.rect.left, self.rect.top - 10, self.image.get_width(), 10
        )
        self.health_bar_colour = "green"
        self.health_bar_outline = self.health_bar.inflate((3, 3))

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

    def update(
        self, dt: float, max_rect: pg.Rect, target: Entity, chase_distance: int
    ) -> None:
        super().update(dt)
        self.position = super().clamp(
            self.position, pg.Vector2(), pg.Vector2(max_rect.size)
        )

        roam_dest = pg.Vector2(get_random_position(
            self.position,
            self.image.get_size(),
            0,
            max_rect,
            self.matrix,
            self.tile_x,
            self.tile_y,
        ))

        if not self.path:
            self.path = self.find_path(roam_dest, "roam")

        distance = self.position.distance_to(target.position)

        if self.path[0]:
            end_pos = self.path[0][-1]
            end_pos = pg.Vector2(end_pos.x * self.tile_x, end_pos.y * self.tile_y)
            target_to_end_dist = end_pos.distance_to(target.position)
        else:
            target_to_end_dist = float("inf")

        if distance < chase_distance:
            if (
                self.path[1] != "chase"
                or len(self.path[0]) == 0
                or target_to_end_dist >= 120
            ):
                self.path = self.find_path(target.position, "chase")

        else:
            if self.path[1] != "roam" or len(self.path[0]) == 0:
                roam_dest = pg.Vector2(roam_dest)
                self.path = self.find_path(roam_dest, "roam")

        if self.path[0]:
            point = self.path[0][0]
            self.target_pos = pg.Vector2(point.x * self.tile_x, point.y * self.tile_y)
            direction = self.target_pos - self.position

            if self.path[1] == "roam":
                self.velocity = 0.5
            else:
                self.velocity = 1

            self.velocity *= direction

            if self.rect.collidepoint(self.target_pos):
                self.path[0].pop(0)

        ratio = self.health / self.max_health

        self.health_bar.center = (self.rect.centerx, self.rect.top - 12)
        self.health_bar.width = self.image.get_width() * ratio
        self.health_bar_outline.center = self.health_bar.center

        if ratio > 0.75:
            self.health_bar_colour = "green"
        elif ratio > 0.50:
            self.health_bar_colour = "orange"
        elif ratio > 0.25:
            self.health_bar_colour = "yellow"
        else:
            self.health_bar_colour = "red"

    def draw(self, screen):
        super().draw(screen)
        pg.draw.rect(screen, self.health_bar_colour, self.health_bar)
        pg.draw.rect(screen, "black", self.health_bar_outline, 3)

    def collision(self, collide_rect: pg.Rect) -> bool:
        return self.rect.colliderect(collide_rect)
