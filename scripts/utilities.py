import pygame as pg
from os import path, listdir
from .settings import BASE_IMAGE_PATH


def load_image(image_path: str, colorkey: pg.Color, alpha: bool = False) -> pg.Surface:
    image = pg.image.load(BASE_IMAGE_PATH + image_path)
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


def cache_angles(image: pg.Surface) -> dict:
    dict_cache = {}
    for angle in range(-180, 181):
        dict_cache[int(angle)] = pg.transform.rotate(image, angle)

    return dict_cache


# def cache_text(font: pg.font.Font) -> dict:
#     cache = {}
#     for chars in [
#     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
#     'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
#     '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
# ]:
#         char = font.render(char, True, colour)