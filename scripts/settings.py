import pygame as pg

from scripts.gui_elements import DropDown


class Settings:
    def __init__(self, screen: pg.Surface) -> None:
        self.screen = screen
        self.w, self.h = self.screen.get_size()

        self.font = pg.Font(size=32)

        self.fps_dropdown = DropDown(
            "FPS: ",
            (self.w // 2, self.h // 5),
            (150, 30),
            "Uncapped",
            [30, 60, 90, 120, 240, "Uncapped"],
            self.font,
            "black",
        )
        self.dropdowns = [self.fps_dropdown]

        self.fps = 0

    def update(self) -> None:
        for dropdown in self.dropdowns:
            dropdown.manage_open()
            option = dropdown.clicked()
            if option:
                if dropdown.name == "FPS: ":
                    if option == "Uncapped":
                        self.fps = 0
                    else:
                        self.fps = int(option)

    def render(self, display: pg.Surface) -> None:
        for dropdown in self.dropdowns:
            dropdown.draw(display)
