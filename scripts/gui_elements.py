import pygame as pg
from pygame.typing import ColorLike, Point


class Button:
    def __init__(
        self,
        image: pg.Surface,
        position: Point,
        sound: pg.Sound | None = None,
        surround_size: Point | None = None,
    ) -> None:
        self.image = image
        self.rect = image.get_rect(center=position)
        if surround_size is not None:
            self.surround_rect = pg.Rect(0, 0, *surround_size)
        else:
            self.surround_rect = pg.Rect(0, 0, 300, 70)

        self.surround_rect.center = position

        self.sound = sound

        self.show_outline = False

    def hovered(self) -> bool:
        hovered = self.rect.collidepoint(pg.mouse.get_pos())
        if hovered:
            self.show_outline = True
        else:
            self.show_outline = False

        return hovered

    def clicked(self) -> bool:
        clicked = pg.mouse.get_just_pressed()[0] if self.hovered() else False
        if clicked and self.sound is not None:
            self.sound.play()

        return clicked

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.image, self.rect)
        if self.show_outline:
            pg.draw.rect(screen, "black", self.surround_rect, 4)


class DropDown:
    def __init__(
        self,
        name: str,
        position: Point,
        size: Point,
        default_option: str,
        options: list,
        font: pg.Font,
        colour: ColorLike,
        bg_colour: ColorLike = "white",
    ) -> None:
        self.name = name
        self.name_surf = font.render(str(name), True, colour, bg_colour)
        self.name_rect = self.name_surf.get_rect(center=position)
        self.name_surround_rect = self.name_rect.inflate(
            (size[0] - self.name_rect.width),
            (size[1] - self.name_rect.height),
        )

        self.main_option_surf = font.render(default_option, True, colour, bg_colour)
        self.main_option_surf_rect = self.main_option_surf.get_rect(
            center=(position[0] + self.name_surround_rect.width, position[1])
        )

        self.main_option_rect = pg.Rect(0, 0, *size)
        self.main_option_rect.center = self.main_option_surf_rect.center

        self.options = list(options)
        self.options_items = []
        for idx, option in enumerate(self.options):
            rect = pg.Rect(0, 0, *size)
            rect.center = (
                self.main_option_rect.centerx,
                self.main_option_rect.centery
                + (self.main_option_rect.height * (idx + 1)),
            )

            surf = font.render(str(option), True, colour, bg_colour)
            surf_rect = surf.get_rect(center=rect.center)

            self.options_items.append([rect, surf, surf_rect])

        self.font = font

        self.colour = colour
        self.bg_colour = bg_colour

        self.open = False

    def manage_open(self) -> None:
        if self.main_option_rect.collidepoint(pg.mouse.get_pos()):
            if pg.mouse.get_just_pressed()[0]:
                self.open = not self.open

    def clicked(self) -> bool | str:
        if not self.open:
            return False

        mpos = pg.mouse.get_pos()

        for idx, opts in enumerate(self.options_items):
            rect = opts[0]
            if rect.collidepoint(mpos):
                if pg.mouse.get_just_pressed()[0]:
                    option = str(self.options[idx])
                    self.open = False
                    self.main_option_surf = self.font.render(
                        option,
                        True,
                        self.colour,
                        self.bg_colour,
                    )
                    self.main_option_surf_rect = self.main_option_surf.get_rect(
                        center=(
                            self.name_surround_rect.centerx
                            + self.name_surround_rect.width,
                            self.name_surround_rect.centery,
                        )
                    )
                    self.main_option_rect.center = self.main_option_surf_rect.center
                    return option

        return False

    def draw(self, screen: pg.Surface) -> None:
        pg.draw.rect(screen, self.bg_colour, self.name_surround_rect)
        pg.draw.rect(screen, self.colour, self.name_surround_rect, 2)
        screen.blit(
            self.name_surf,
            self.name_rect,
        )

        pg.draw.rect(screen, self.bg_colour, self.main_option_rect)
        pg.draw.rect(screen, self.colour, self.main_option_rect, 2)
        screen.blit(
            self.main_option_surf,
            self.main_option_surf_rect,
        )

        if self.open:
            for rect, surf, surf_rect in self.options_items:
                pg.draw.rect(screen, self.bg_colour, rect)
                pg.draw.rect(screen, self.colour, rect, 2)
                screen.blit(
                    surf,
                    surf_rect,
                )
