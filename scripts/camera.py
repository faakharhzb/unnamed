import pygame as pg


class Camera:
    def __init__(
        self,
        focus: pg.sprite.Sprite,
        background_pos: pg.Vector2,
    ) -> None:
        self.focus = focus
        self.background_pos = background_pos

    def apply_offset(self, all_sprites: pg.sprite.Group) -> tuple[pg.sprite.Group, pg.Vector2]:
        for entity in all_sprites:
            entity.position -= self.focus.velocity

        self.background_pos -= self.focus.velocity

        return all_sprites, self.background_pos
