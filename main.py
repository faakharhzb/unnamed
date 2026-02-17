from types import NoneType
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

        self.fps_font = pg.Font(size=33)
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
                120,
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

        self.prev_fps = 0
        self.fps_text = pg.Surface((10, 10))

        self.prev_ammo = 0
        self.ammo_text = pg.Surface((10, 10))

        self.prev_kills = 0
        self.kills_text = pg.Surface((10, 10))

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
            ammo_surface = pg.Surface((60, 60))
            ammo_surface.fill("red")
            ammo = Obtainable_Item(
                ammo_surface,
                get_random_position(
                    pg.Vector2(),
                    ammo_surface.get_size(),
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
                10,
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

    def main_game(self) -> None:
        self.mousepos = pg.mouse.get_pos()

        if self.enemy is not None:
            if self.enemy.collision(self.player.rect):
                self.running = False

        if pg.time.get_ticks() - self.ammo_delay >= 6000:
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
                if isinstance(self.enemy, NoneType):
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
            self.enemy.update(self.dt, self.bg_rect, self.player, 350)

        if self.player.moved:
            self.player.set_state("running")
        else:
            self.player.set_state("idle")

    async def main(self) -> None:
        self.running = True
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            self.dt = (self.clock.tick() / 1000) * 60
            await asyncio.sleep(0)

            self.main_game()

            # self.all_sprites, self.bg_position = self.camera.apply_offset(
            #     self.all_sprites
            # )

            self.bg_rect.topleft = self.bg_position.xy

            self.screen.blit(self.background, self.bg_position)

            for entity in self.all_sprites:
                entity.draw(self.screen)

            fps = f"{round(self.clock.get_fps())} FPS"
            if fps != self.prev_fps:
                self.fps_text = self.fps_font.render(fps, True, "white")

            self.screen.blit(self.fps_text, (5, 0))
            ammo = f"Ammo: {self.player.ammo}"
            if ammo != self.prev_ammo:
                self.ammo_text = self.fps_font.render(ammo, True, "white")

            self.screen.blit(self.ammo_text, (5, 50))

            kills = f"Kills: {self.player.kill_count}"
            if kills != self.prev_kills:
                self.kills_text = self.fps_font.render(kills, True, "white")

            self.screen.blit(
                self.kills_text,
                (self.w - (self.kills_text.get_width() + 10), 0),
            )

            # for row in range(self.rows):
            #     for col in range(self.cols):
            #         value = self.matrix[row][col]
            #         x = col * self.tile_x
            #         y = row * self.tile_y
            #
            #         if value == 0:
            #             rect = pg.Rect(x, y, self.tile_x, self.tile_y)
            #             pg.draw.rect(self.screen, (255, 255, 255, 255), rect)

            # for point in self.enemy.path[0]:
            #     pg.draw.circle(
            #         self.screen,
            #         "black",
            #         (
            #             point.x * self.tile_x,
            #             point.y * self.tile_y,
            #         ),
            #         8,
            #     )
            # try:
            #     point = self.enemy.path[0][0]
            #     pg.draw.circle(
            #         self.screen,
            #         "orange",
            #         (point.x * self.tile_x, point.y * self.tile_y),
            #         8,
            #     )
            # except:
            #     pass
            #
            # for col in range(self.cols + 1):
            #     x = col * self.tile_x
            #     pg.draw.line(self.screen, "purple", (x, 0), (x, self.h), 1)
            #
            # for row in range(self.rows + 1):
            #     y = row * self.tile_y
            #     pg.draw.line(self.screen, "purple", (0, y), (self.w, y), 1)
            #
            # pg.draw.rect(self.screen, "red", self.enemy.rect, 1)
            # pg.draw.rect(self.screen, "blue", self.player.rect, 4)

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
