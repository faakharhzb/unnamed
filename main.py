import numpy as np
import pygame as pg
import moderngl as mgl

import sys
import os

from scripts.utilities import load_image
from scripts.gamestate import GameState
from scripts.game import Game
from scripts.main_menu import MainMenu
from scripts.settings import Settings


class Main:
    def __init__(
        self,
        matrix: np.ndarray | list,
        tile_x: int,
        tile_y: int,
        rows: int,
        cols: int,
    ) -> None:
        self.matrix = matrix
        self.tile_x, self.tile_y = tile_x + 1, tile_y + 1
        self.rows, self.cols = rows, cols

        pg.init()

        pg.display.set_caption("Unnamed Game")
        self.screen = pg.display.set_mode((1280, 720))
        self.w, self.h = self.screen.get_size()

        self.background = load_image("background.png", "white", scale=8)
        self.bg_position = pg.Vector2()
        self.bg_rect = self.background.get_rect(topleft=(0, 0))

        self.clock = pg.time.Clock()
        self.game_start_delay = 0

        self.fps_text = pg.Surface((10, 10))
        self.prev_fps = 0
        self.fps_update_delay = pg.time.get_ticks()

        self.game = Game(
            matrix,
            tile_x,
            tile_y,
            rows,
            cols,
            self.screen,
            self.game_start_delay,
            self.bg_rect,
        )
        self.main_menu = MainMenu(self.screen)
        self.settings = Settings(self.screen)

        self.game_state = GameState.main_menu

    def main(self) -> None:
        self.running = True
        while self.running:
            self.screen.fill("white")

            self.screen.blit(self.background)

            if self.game_state == GameState.game:
                self.running = self.game.update(self.dt)
                self.game.render(self.screen)
            elif self.game_state == GameState.main_menu:
                self.game_state, self.running, self.game_start_delay = (
                    self.main_menu.update()
                )
                self.main_menu.render(self.screen)

                self.game.game_start_delay = self.game_start_delay
            elif self.game_state == GameState.settings:
                self.settings.update()
                self.settings.render(self.screen)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        if self.game_state in [
                            GameState.game,
                            GameState.settings,
                        ]:
                            self.game_state = GameState.main_menu

            self.dt = (self.clock.tick(self.settings.fps) / 1000) * 60

            if pg.time.get_ticks() - self.fps_update_delay >= 500:
                fps = f"{round(self.clock.get_fps())} FPS"
                if fps != self.prev_fps:
                    self.fps_text = self.game.fps_font.render(
                        fps, True, (50, 20, 150)
                    )

                    self.prev_fps = fps

                self.fps_update_delay = pg.time.get_ticks()

            self.screen.blit(
                self.fps_text,
                (
                    self.w - (self.fps_text.get_width() + 10),
                    0,
                ),
            )

            pg.display.flip()

        pg.quit()
        sys.exit()


if __name__ == "__main__":
    matrix = np.load(
        os.path.join(
            os.path.dirname(sys.argv[0]), "assets", "pathfinding_grid.npy"
        )
    )
    main = Main(matrix, 32, 18, 40, 40)
    main.main()
