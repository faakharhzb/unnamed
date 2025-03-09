import pygame as pg
import time
from os import listdir, path

def load_image(image_path: str, colorkey: int = None) -> pg.Surface:
    image = pg.image.load(image_path).convert()
    image.set_colorkey(colorkey)
    return image

def load_images(image_dir: str, colorkey: int = None) -> list[pg.Surface]:
    return [load_image(image_path, colorkey) for image_path in sorted(listdir(image_dir))]


def show_text(font: pg.font.Font, pos: int, color: pg.Color, text: str, surf: pg.Surface):
		 text_surf = font.render(text, True, color)
    surf.blit(text_surf, pos)
    