import pygame as pg
<<<<<<< HEAD
from os import path, listdir
=======
import os
>>>>>>> temp-branch


def load_image(
    image_path: str, colorkey: pg.Color, alpha: bool = False, scale: float = 1
) -> pg.Surface:
<<<<<<< HEAD
    image = pg.transform.scale_by(pg.image.load("./assets/images/" + image_path), scale)
=======
    image = pg.transform.scale_by(
        pg.image.load("./assets/images/" + image_path), scale
    )
>>>>>>> temp-branch
    image.set_colorkey(colorkey) if not alpha else False
    return image.convert_alpha() if alpha else image.convert()


def load_images(image_folder: str, colorkey: int) -> list:
    return [
        load_image(os.path.join(image_folder, image), colorkey)
        for image in sorted(os.listdir(image_folder))
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
