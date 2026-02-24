import pygame as pg
from numpy import ndarray
import os
import random

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
    image = image.convert_alpha() if alpha else image.convert()
    return image


def load_images(
    image_path: str,
    colorkey: pg.Color,
    alpha: bool = False,
    scale: float | tuple[float, float] = 1,
) -> list[pg.Surface]:
    return [
        load_image(os.path.join(image_path, image), colorkey, alpha, scale)
        for image in sorted(
            os.listdir(os.path.join("./assets/images", image_path))
        )
    ]


def load_audio(audio_path: str, volume: float = 1.0) -> pg.Sound:
    audio_path = os.path.join("./assets/audio", audio_path)
    if not os.path.exists(audio_path):
        raise FileNotFoundError("No such audio file:", audio_path)

    audio = pg.Sound(audio_path)
    audio.set_volume(min(1.0, max(0, volume)))
    return audio


def get_random_position(
    point: pg.Vector2,
    size: Point,
    radius: int,
    max_rect: pg.Rect,
    matrix: ndarray,
    tile_x: int,
    tile_y: int,
) -> tuple[int, int]:
    while True:
        x = random.randint(max_rect.left + size[0], max_rect.right - size[0])
        y = random.randint(max_rect.top + size[1], max_rect.bottom - size[1])

        dist = point.distance_to((x, y))
        if dist < radius:
            continue

        valid = True
        rect = pg.Rect((x, y), size)
        rect.clamp_ip(max_rect)
        for gy in range(rect.top, rect.bottom):
            for gx in range(rect.left, rect.right):
                if matrix[gy // tile_y][gx // tile_x] == 0:
                    valid = False
                    break

            if not valid:
                break

        if not valid:
            continue

        return x, y
