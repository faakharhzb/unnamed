import pygame as pg
import math


from scripts.gui_elements import Button
from scripts.gamestate import GameState
from scripts.utilities import load_audio


class MainMenu:
    def __init__(
        self,
        screen: pg.Surface,
    ) -> None:
        self.screen = screen
        self.w, self.h = self.screen.get_size()

        self.name_font = pg.font.SysFont("Times new roman", 120, True, True)
        self.menu_font = pg.Font(size=50)

        self.name_surf = self.name_font.render(
            pg.display.get_caption()[0], True, "white"
        )

        self.click_sound = load_audio("button_click.ogg", 0.85)

        self.name_x = self.w // 2
        self.name_y = self.h // 5
        self.name_rect = self.name_surf.get_rect(
            center=(self.name_x, self.name_y)
        )

        play_surf = self.menu_font.render(
            "Play Game",
            True,
            "white",
        )

        self.play_button = Button(
            play_surf, (self.w // 2, self.h // 2), self.click_sound
        )
        settings_surf = self.menu_font.render("Settings", True, "white")
        self.settings_button = Button(
            settings_surf,
            (self.w // 2, self.h - self.h / 2.7),
            self.click_sound,
        )

        exit_surf = self.menu_font.render(
            "Exit",
            True,
            "white",
        )
        self.exit_button = Button(
            exit_surf, (self.w // 2, self.h - self.h / 4), self.click_sound
        )

        self.menu_buttons = [
            self.play_button,
            self.settings_button,
            self.exit_button,
        ]

    def update(self) -> tuple[GameState, bool, int, bool]:
        game_state = GameState.main_menu
        running = True
        game_start_delay = 0
        new_game = False

        if self.play_button.clicked():
            game_start_delay = pg.time.get_ticks()
            game_state = GameState.game
            new_game = True
        elif self.settings_button.clicked():
            game_state = GameState.settings
        elif self.exit_button.clicked():
            running = False

        self.name_rect.centery = (
            self.name_y + math.sin(pg.time.get_ticks() * 0.005) * 50
        )

        return game_state, running, game_start_delay, new_game

    def render(self, display: pg.Surface) -> None:
        display.blit(self.name_surf, self.name_rect)

        for button in self.menu_buttons:
            button.draw(display)
