import pygame as pg
import time
from os import listdir, path

def fps_independence(last_time: float) -> float:
    dt = time.time() - last_time
    dt *= 60
    return dt

def load_image(image_path: str, colorkey: int = None) -> pg.Surface:
    image = pg.image.load(image_path).convert()
    image.set_colorkey(colorkey)
    return image

def load_images(image_dir: str, colorkey: int = None) -> list[pg.Surface]:
    return [load_image(image_path, colorkey) for image_path in sorted(listdir(image_dir))]


def show_text(font_size: int, pos: int, color: int, bold: bool = False, italic: bool = False, text: str):
    font = pg.font.SysFont('arial', font_size, bold, italic)
		 font.render(text, True, )