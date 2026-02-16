import pygame as pg
from numpy import ndarray
import os
import random
import math

from pygame.typing import Point


def load_image(
    image_path: str,
    colorkey: pg.Color,
    alpha: bool = False,
    scale: float | tuple[float, float] = 1,
) -> pg.Surface:
    image = pg.image.load(os.path.join("./assets/images", image_path))
    image = pg.transform.scale_by(image, scale)
    image.set_colorkey(colorkey) if not alpha else False
    return image.convert_alpha() if alpha else image.convert()


def load_images(
    image_path: str,
    colorkey: pg.Color,
    alpha: bool = False,
    scale: float | tuple[float, float] = 1,
) -> list[pg.Surface]:
    return [
        load_image(os.path.join(image_path, image), colorkey, alpha, scale)
        for image in sorted(os.listdir(os.path.join("./assets/images", image_path)))
    ]


def get_random_position(
    point: pg.Vector2, size: Point, radius: int, mx: int, my: int, matrix: ndarray
) -> tuple[int, int]:
    while True:
        x = random.randint(0, mx)
        y = random.randint(0, my)

        dist = math.hypot(point.x - x, point.y - y)
        if dist < radius:
            continue

        gx = x // matrix.shape[1]
        gy = y // matrix.shape[0]
        if matrix[gy][gx] == 0:
            continue

        rect = pg.Rect((x, y), size)
        if not (
            0 <= rect.left < mx
            and 0 <= rect.right <= mx
            and 0 <= rect.top < my
            and 0 <= rect.bottom <= my
        ):
            continue

        gw = mx // matrix.shape[1]
        gh = my // matrix.shape[0]

        # Clamp rect edges to matrix bounds
        left = max(0, rect.left // gw)
        right = min(matrix.shape[1] - 1, rect.right // gw)
        top = max(0, rect.top // gh)
        bottom = min(matrix.shape[0] - 1, rect.bottom // gh)

        for gy in range(top, bottom + 1):
            for gx in range(left, right + 1):
                if matrix[gy][gx] == 0:
                    continue

        return x, y
