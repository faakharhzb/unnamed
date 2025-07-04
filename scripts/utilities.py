import pygame as pg
from os import path, listdir
from .settings import BASE_IMAGE_PATH


def load_image(
    image_path: str, colorkey: pg.Color, alpha: bool = False, scale: float = 1
) -> pg.Surface:
    image = pg.transform.scale_by(
        pg.image.load(BASE_IMAGE_PATH + image_path), scale
    )
    image.set_colorkey(colorkey) if not alpha else False
    return image.convert_alpha() if alpha else image.convert()


def load_images(image_folder: str, colorkey: int) -> list:
    return [
        load_image(path.join(image_folder, image), colorkey)
        for image in sorted(listdir(image_folder))
    ]


def show_text(
    text: str,
    font: pg.font.Font,
    color: pg.Color,
    pos: list[int],
    screen: pg.Surface,
) -> None:
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)


def cache_angles(image: pg.Surface) -> dict:
    dict_cache = {}
    for angle in range(-180, 181):
        dict_cache[int(angle)] = pg.transform.rotate(image, angle)

    return dict_cache
