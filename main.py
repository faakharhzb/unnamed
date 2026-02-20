import math
import os
import numpy as np
import pygame as pg

import sys
import random
import asyncio

from scripts.camera import Camera
from scripts.utilities import get_random_position, load_image, load_images
from scripts.entities import Player, Enemy
from scripts.objects import Bullet, Obtainable_Item, Gun
from scripts.gui_elements import Button, DropDown
from scripts.gamestate import GameState


class Main:
    def __init__(
        self,
        matrix: np.ndarray | list,
        tile_x: int,
        tile_y: int,
        rows: int,
        cols: int,
    ) -> None:
        pg.init()

        pg.display.set_caption("Unnamed Game")
        self.screen = pg.display.set_mode((1280, 720))
        self.w, self.h = self.screen.get_size()

        self.images = {
            "player_idle": load_images("player/idle", "white", scale=(5, 6)),
            "player_running": load_images(
                "player/running", "white", scale=(5, 6)
            ),
            "enemy": load_image("enemy.png", "white", scale=1.1),
            "rifle": load_image("guns/rifle.png", "white", scale=2.75),
            "background": load_image("background.png", "white"),
            "bullet": load_image("bullet.png", "white", scale=2),
            "ammo": load_image("ammo.png", "white"),
        }
        self.audio = {
            "gunshot": pg.mixer.Sound("assets/audio/gunshot.ogg"),
            "empty_gun": pg.mixer.Sound("assets/audio/empty_gun.ogg"),
            "reload": pg.mixer.Sound("assets/audio/reload.ogg"),
        }
        self.background = pg.transform.scale(
            self.images["background"], (self.w, self.h)
        )
        self.bg_position = pg.Vector2()
        self.bg_rect = self.background.get_rect(topleft=(0, 0))

        self.images["ammo"] = pg.transform.scale(self.images["ammo"], (60, 60))

        self.fps_font = pg.Font(size=33)
        self.name_font = pg.font.SysFont("Times new roman", 120, True, True)
        self.menu_font = pg.Font(size=60)
        self.clock = pg.time.Clock()

        self.mousepos = pg.mouse.get_pos()

        self.player_images = {
            "idle": self.images["player_idle"],
            "running": self.images["player_running"],
        }
        self.player = Player(
            [self.w // 2, self.h // 2],
            self.player_images,
            6,
            matrix,
            tile_x,
            tile_y,
            rows,
            cols,
        )
        self.rifle = Gun(self.images["rifle"], self.player.rect.center)
        self.enemy = Enemy(
            get_random_position(
                self.player.position,
                self.images["enemy"].get_size(),
                325,
                self.bg_rect,
                matrix,
                tile_x,
                tile_y,
            ),
            self.images["enemy"],
            self.player.base_speed - 1.3,
            matrix,
            tile_x,
            tile_y,
            rows,
            cols,
        )

        self.camera = Camera(self.player, self.bg_position)

        self.all_sprites = pg.sprite.Group(self.player, self.rifle, self.enemy)
        self.bullets = pg.sprite.Group()
        self.ammos = pg.sprite.Group()

        self.dt = 0.017
        self.bullet_cooldown = pg.time.get_ticks()
        self.ammo_delay = pg.time.get_ticks()
        self.new_enemy_delay = pg.time.get_ticks()

        self.running = True
        self.spawn_new_enemy = False

        self.matrix = matrix
        self.tile_x, self.tile_y = tile_x + 1, tile_y + 1
        self.rows, self.cols = rows, cols

        self.fps = 0

        self.prev_fps = 0
        self.fps_text = pg.Surface((10, 10))

        self.prev_ammo = 0
        self.ammo_text = pg.Surface((10, 10))

        self.prev_kills = 0
        self.kills_text = pg.Surface((10, 10))

        self.name_surf = self.name_font.render(
            pg.display.get_caption()[0], True, "white"
        )

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
        self.play_button = Button(play_surf, (self.w // 2, self.h // 2))

        settings_surf = self.menu_font.render(
            "Settings",
            True,
            "white",
        )
        self.settings_button = Button(
            settings_surf, (self.w // 2, self.h - self.h / 2.7)
        )

        exit_surf = self.menu_font.render(
            "Exit",
            True,
            "white",
        )
        self.exit_button = Button(
            exit_surf, (self.w // 2, self.h - self.h / 4)
        )

        self.menu_buttons = [
            self.play_button,
            self.settings_button,
            self.exit_button,
        ]

        self.fps_dropdown = DropDown(
            "FPS: ",
            (self.w // 4, self.h // 2),
            (150, 50),
            "Uncapped",
            [30, 60, 90, 120, 240, "Uncapped"],
            self.fps_font,
            "black",
        )
        self.dropdowns = [self.fps_dropdown]

        self.game_state = GameState.menu

    def shoot(self) -> None:
        self.mousepos = pg.mouse.get_pos()

        if pg.time.get_ticks() - self.bullet_cooldown >= 170:
            bullet = Bullet(
                self.images["bullet"],
                self.player.position.xy,
                self.rifle.angle,
                25,
            )
            self.player.ammo -= 1
            self.bullets.add(bullet)
            self.all_sprites.add(bullet)
            self.bullet_cooldown = pg.time.get_ticks()

            sound = self.audio["gunshot"]
            sound.set_volume(0.5)
            sound.play()

    def spawn_ammo(self) -> None:
        if len(self.ammos) < 4:
            ammo = Obtainable_Item(
                self.images["ammo"],
                get_random_position(
                    pg.Vector2(),
                    self.images["ammo"].get_size(),
                    0,
                    self.bg_rect,
                    self.matrix,
                    self.tile_x,
                    self.tile_y,
                ),
            )
            self.all_sprites.add(ammo)
            self.ammos.add(ammo)

    def spawn_enemy(self) -> None:
        self.enemy = Enemy(
            get_random_position(
                self.player.position,
                self.images["enemy"].get_size(),
                325,
                self.bg_rect,
                self.matrix,
                self.tile_x,
                self.tile_y,
            ),
            self.images["enemy"],
            self.player.base_speed - 1.3,
            self.matrix,
            self.tile_x,
            self.tile_y,
            self.rows,
            self.cols,
        )
        self.enemy.add(self.all_sprites)
        self.spawn_new_enemy = False

    def manage_hit(self) -> None:
        self.enemy.health -= 1
        if self.enemy.health <= 0:
            self.player.kill_count += 1
            self.enemy.kill()

            self.new_enemy_delay = pg.time.get_ticks()
            self.spawn_new_enemy = True
            self.enemy = None

    def settings(self) -> None:
        self.background.set_alpha(150)

        for dropdown in self.dropdowns:
            dropdown.manage_open()
            option = dropdown.clicked()
            if option:
                if dropdown.name == "FPS: ":
                    if option == "Uncapped":
                        self.fps = 0
                    else:
                        self.fps = int(option)

            dropdown.draw(self.screen)

    def menu(self) -> None:
        self.background.set_alpha(150)

        if self.play_button.clicked():
            self.game_start_delay = pg.time.get_ticks()
            self.game_state = GameState.main_game
        elif self.settings_button.clicked():
            self.game_state = GameState.settings
        elif self.exit_button.clicked():
            self.running = False

        self.name_rect.centery = (
            self.name_y + math.sin(pg.time.get_ticks() * 0.005) * 50
        )

        self.screen.blit(self.name_surf, self.name_rect)

        for button in self.menu_buttons:
            button.draw(self.screen)

    def main_game(self) -> None:
        if pg.time.get_ticks() - self.game_start_delay <= 250:
            return

        self.background.set_alpha(255)
        self.mousepos = pg.mouse.get_pos()

        if self.enemy is not None:
            if self.enemy.collision(self.player.rect):
                self.running = False

        if pg.time.get_ticks() - self.ammo_delay >= 6700:
            self.spawn_ammo()
            self.ammo_delay = pg.time.get_ticks()

        for ammo in self.ammos:
            if ammo.collision(self.player.rect):
                self.all_sprites.remove(ammo)
                self.ammos.remove(ammo)
                self.player.ammo += 12

                sound = self.audio["reload"]
                sound.set_volume(0.7)
                sound.play()

        if pg.mouse.get_pressed() == (1, 0, 0):
            if self.player.ammo >= 1:
                self.shoot()
            else:
                sound = self.audio["empty_gun"]
                sound.set_volume(0.7)
                sound.play()

        if self.enemy is not None:
            for bullet in self.bullets:
                if self.enemy is None:
                    break

                bullet.update(self.bg_rect, self.dt)
                if bullet.hit(self.enemy.rect):
                    self.manage_hit()
                    bullet.kill()

        if self.spawn_new_enemy:
            if pg.time.get_ticks() - self.new_enemy_delay >= random.randint(
                200, 4000
            ):
                self.spawn_enemy()

        self.player.update(self.dt, self.bg_rect)
        self.rifle.update(
            self.player.position,
        )

        if self.enemy is not None:
            self.enemy.update(self.dt, self.bg_rect, self.player, 425)

        if self.player.moved:
            self.player.set_state("running")
        else:
            self.player.set_state("idle")

        for entity in self.all_sprites:
            entity.draw(self.screen)

        fps = f"{round(self.clock.get_fps())} FPS"
        if fps != self.prev_fps:
            self.fps_text = self.fps_font.render(fps, True, "white")

        self.prev_fps = fps

        self.screen.blit(self.fps_text, (5, 0))
        ammo = f"Ammo: {self.player.ammo}"
        if ammo != self.prev_ammo:
            self.ammo_text = self.fps_font.render(ammo, True, "white")

        self.prev_ammo = ammo

        self.screen.blit(self.ammo_text, (5, 50))

        kills = f"Kills: {self.player.kill_count}"
        if kills != self.prev_kills:
            self.kills_text = self.fps_font.render(kills, True, "white")

        self.prev_kills = kills

        self.screen.blit(
            self.kills_text,
            (self.w - (self.kills_text.get_width() + 10), 0),
        )

    async def main(self) -> None:
        self.running = True
        while self.running:
            self.screen.fill("white")
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        if self.game_state in [
                            GameState.main_game,
                            GameState.settings,
                        ]:
                            self.game_state = GameState.menu

            self.dt = (self.clock.tick(self.fps) / 1000) * 60

            self.bg_rect.topleft = self.bg_position.xy
            self.screen.blit(self.background, self.bg_position)

            if self.game_state == GameState.main_game:
                self.main_game()
            elif self.game_state == GameState.menu:
                self.menu()
            elif self.game_state == GameState.settings:
                self.settings()

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
    asyncio.run(main.main())
