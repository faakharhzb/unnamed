import pygame as pg
import moderngl
import os

def get_texture(surf: pg.Surface, ctx: moderngl.Context) -> moderngl.Texture:
    texture = ctx.texture(
            surf.get_size(), 4, surf.get_view("1")
        )
    texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
    texture.swizzle = "BGRA"

    return texture

def load_texture(
    image_path: str, colorkey: pg.Color, alpha: bool = False, scale: float = 1, ctx: moderngl.Context
) -> moderngl.Texture:
    surf = pg.transform.scale_by(
        pg.image.load("./assets/images/" + image_path), scale
    )
    surf.set_colorkey(colorkey) if not alpha else False
    surf = surf.convert_alpha() if alpha else surf.convert()

    return get_texture(surf, ctx)


def load_textures(image_folder: str, colorkey: int, ctx: moderngl.Context) -> list:
    return [
        load_texture(os.path.join(image_folder, image), colorkey, ctx=ctx)
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
