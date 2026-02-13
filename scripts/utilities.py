import pygame as pg
import os


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


def show_text(
    text: str,
    font: pg.font.Font,
    color: pg.Color,
    pos: list[int],
    screen: pg.Surface,
) -> None:
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)
