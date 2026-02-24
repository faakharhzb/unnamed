import pygame as pg

from scripts.gui_elements import Button
from scripts.gamestate import GameState
from scripts.utilities import load_audio


class PauseMenu:
    def __init__(
        self,
        screen: pg.Surface,
    ) -> None:
        self.screen = screen
        self.w, self.h = self.screen.get_size()

        self.title_font = pg.font.SysFont("Times new roman", 120, True, True)
        self.menu_font = pg.Font(size=50)

        self.title_surf = self.title_font.render("Game Paused", True, "white")

        self.click_sound = load_audio("button_click.ogg", 0.85)

        self.title_x = self.w // 2
        self.title_y = self.h // 5
        self.title_rect = self.title_surf.get_rect(
            center=(self.title_x, self.title_y)
        )

        resume_surf = self.menu_font.render(
            "Resume Game",
            True,
            "white",
        )

        self.resume_button = Button(
            resume_surf, (self.w // 2, self.h // 2), self.click_sound
        )
        back_to_main_surf = self.menu_font.render(
            "Exit",
            True,
            "white",
        )
        self.back_to_main_button = Button(
            back_to_main_surf,
            (self.w // 2, self.h - self.h / 2.7),
            self.click_sound,
        )

        self.menu_buttons = [
            self.resume_button,
            self.back_to_main_button,
        ]

    def update(self) -> tuple[GameState, int]:
        game_state = GameState.pause_menu
        game_start_delay = 0

        if self.resume_button.clicked():
            game_start_delay = pg.time.get_ticks()
            game_state = GameState.game
        elif self.back_to_main_button.clicked():
            game_state = GameState.main_menu

        return game_state, game_start_delay

    def render(self, display: pg.Surface) -> None:
        display.blit(self.title_surf, self.title_rect)

        for button in self.menu_buttons:
            button.draw(display)
