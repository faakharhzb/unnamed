import pygame as pg
from pygame.typing import ColorLike, Point


class Button:
    def __init__(
        self,
        image: pg.Surface,
        position: Point,
        sound: pg.Sound | None = None,
        show_surround: bool = True,
        surround_size: Point | None = None,
    ) -> None:
        self.image = image
        self.rect = image.get_rect(center=position)
        if surround_size is not None:
            self.surround_rect = pg.Rect(0, 0, *surround_size)
            self.surround_rect.center = position
        elif surround_size is None and show_surround:
            self.surround_rect = pg.Rect(0, 0, 300, 70)
            self.surround_rect.center = position
        else:
            self.surround_rect = None

        self.sound = sound

        self.show_outline = False
        self.show_surround = show_surround

    def hovered(self) -> bool:
        rect = self.surround_rect if self.show_surround else self.rect
        hovered = rect.collidepoint(pg.mouse.get_pos())
        if hovered and self.show_surround:
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
        sound: pg.Sound = None,
    ) -> None:
        self.name = name
        self.font = font
        self.colour = colour
        self.bg_colour = bg_colour
        self.sound = sound

        self.name_surf = font.render(str(name), True, colour, bg_colour)
        self.name_button = Button(self.name_surf, position, sound, False)
        self.name_surround_rect = self.name_button.rect.inflate(
            (size[0] - self.name_button.rect.width),
            (size[1] - self.name_button.rect.height),
        )

        main_option_surf = font.render(default_option, True, colour, bg_colour)
        self.main_option_button = Button(
            main_option_surf,
            (position[0] + self.name_surround_rect.width, position[1]),
            sound,
            False,
        )
        self.main_option_rect = pg.Rect(0, 0, *size)
        self.main_option_rect.center = self.main_option_button.rect.center

        self.options = list(options)
        self.option_buttons = []
        for idx, option in enumerate(self.options):
            rect = pg.Rect(0, 0, *size)
            rect.center = (
                self.main_option_rect.centerx,
                self.main_option_rect.centery
                + (self.main_option_rect.height * (idx + 1)),
            )

            surf = font.render(str(option), True, colour, bg_colour)
            button = Button(surf, rect.center, sound, True, size)
            self.option_buttons.append(button)

        self.open = False

    def manage_open(self) -> None:
        if self.main_option_rect.collidepoint(pg.mouse.get_pos()):
            if pg.mouse.get_just_pressed()[0]:
                self.open = not self.open

    def clicked(self) -> bool | str:
        if not self.open:
            return False

        for idx, button in enumerate(self.option_buttons):
            if button.clicked():
                option = str(self.options[idx])
                self.open = False

                main_option_surf = self.font.render(
                    option, True, self.colour, self.bg_colour
                )

                self.main_option_button.image = main_option_surf
                self.main_option_button.rect.size = main_option_surf.get_size()
                self.main_option_button.rect.center = self.main_option_rect.center
                return option

        return False

    def draw(self, screen: pg.Surface) -> None:
        pg.draw.rect(screen, self.bg_colour, self.name_surround_rect)
        pg.draw.rect(screen, self.colour, self.name_surround_rect, 2)
        screen.blit(self.name_surf, self.name_button.rect)

        pg.draw.rect(screen, self.bg_colour, self.main_option_rect)
        pg.draw.rect(screen, self.colour, self.main_option_rect, 2)
        self.main_option_button.draw(screen)

        if self.open:
            for button in self.option_buttons:
                rect = button.surround_rect
                pg.draw.rect(screen, self.bg_colour, rect)

                button.draw(screen)
