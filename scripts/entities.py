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

<<<<<<< HEAD
    def clamp(self, w: int, h: int) -> None:
        super().clamp(w, h)

=======
>>>>>>> temp-branch
    def update(self, dt: float, w: int, h: int) -> None:
        super().update(dt)
        self.position = super().clamp(self.position, pg.Vector2(0, 0), pg.Vector2(w, h))

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
<<<<<<< HEAD
=======
        tile_x: int,
        tile_y: int,
>>>>>>> temp-branch
        rows: int,
        cols: int,
    ) -> None:
        super().__init__(pos, image, base_speed)

        self.rows = rows
        self.cols = cols

        self.base_speed = base_speed
        self.velocity = [self.base_speed, 0]
        self.matrix = matrix
        self.tile_x, self.tile_y = tile_x, tile_y

        self.grid = Grid(matrix=self.matrix)
        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

<<<<<<< HEAD
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
=======
        self.arrived = []
        self.path = [[], ""]

        self.target_pos = pg.Vector2()
        self.rows, self.cols = rows, cols

    def find_path(self, target_pos: pg.Vector2, reason: str) -> list[GridNode, str]:
        self.start = self.grid.node(
            min(int(self.position.x // self.tile_x), self.rows - 1),
            min(int(self.position.y // self.tile_y), self.cols - 1),
        )

        self.end = self.grid.node(
            min(int(target_pos.x // self.tile_x), self.rows - 1),
            min(int(target_pos.y // self.tile_y), self.cols - 1),
>>>>>>> temp-branch
        )

        path, _ = self.finder.find_path(self.start, self.end, self.grid)
        return [path, reason]

    def get_angle(self, target_pos: pg.Vector2) -> int:
        angle = math.degrees(
            math.atan2(
<<<<<<< HEAD
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
=======
                target_pos.y - self.position.y,
                target_pos.x - self.position.x,
            )
        )

        return angle

    def update(
        self, dt: float, w: int, h: int, target: Entity, chase_distance: int
    ) -> None:
        super().update(dt)
        self.position = super().clamp(self.position, pg.Vector2(), pg.Vector2(w, h))

        if not self.path:
            self.path = self.find_path(target.position, "roam")

        distance = math.hypot(
            self.position.x - target.position.x,
            self.position.y - target.position.y,
        )
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
                self.velocity = pg.Vector2(self.speed).rotate(angle)
            else:
                self.velocity = pg.Vector2(self.speed - 0.5).rotate(angle)

            if self.rect.collidepoint(self.target_pos):
                self.path[0].pop(0)
>>>>>>> temp-branch

    def draw(self, screen):
        super().draw(screen)

    def collision(self, collide_rect: pg.Rect) -> bool:
        return self.rect.colliderect(collide_rect)
