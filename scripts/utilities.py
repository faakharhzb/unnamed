import pygame as pg
from os import path, listdir


def load_image(image_path: str, colorkey: pg.Color, alpha: bool = False) -> pg.Surface:
    image = pg.image.load(image_path)
    image.set_colorkey(colorkey) if not alpha else False
    return image.convert_alpha() if alpha else image.convert()


def load_images(image_folder: str, colorkey: int) -> list:
    return [
        load_image(path.join(image_folder, image), colorkey)
        for image in sorted(listdir(image_folder))
    ]


def show_text(
    text: str, font: pg.font.Font, color: pg.Color, pos: list[int], screen: pg.Surface
) -> None:
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)
