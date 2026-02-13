import numpy as np
import pygame as pg

import sys
import random
import asyncio

from scripts.utilities import show_text, load_image, load_images
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
            "rifle": load_image("guns/rifle.png", "white", scale=(2, 1.4)),
            "background": load_image("background.png", "white"),
            "bullet": load_image("bullet.png", "white", scale=2),
        }
        # TODO: Add player animation
        self.background = pg.transform.scale(
            self.images["background"], (self.w, self.h)
        )

        self.fps_font = pg.font.SysFont("arial", 20)
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
        )
        self.rifle = Gun(self.images["rifle"], self.player.rect.center)
        self.enemy = Enemy(
            [
                random.randint(10, self.w - 10),
                random.randint(10, self.h - 10),
            ],
            self.images["enemy"],
            self.player.base_speed - 1.5,
            matrix,
            tile_x,
            tile_y,
            rows,
            cols,
        )

        self.all_sprites = pg.sprite.Group(self.player, self.rifle, self.enemy)
        self.bullets = pg.sprite.Group()
        self.ammos = pg.sprite.Group()

        self.dt = 0.017
        self.bullet_cooldown = pg.time.get_ticks()
        self.ammo_delay = pg.time.get_ticks()

        self.running = True

        self.matrix = matrix
        self.tile_x, self.tile_y = tile_x + 1, tile_y + 1
        self.rows, self.cols = rows, cols

        self.prev_fps = 0
        self.fps_text = pg.Surface((10, 10))

        self.prev_ammo = 0
        self.ammo_text = pg.Surface((10, 10))

    def shoot(self) -> None:
        self.mousepos = pg.mouse.get_pos()

        if pg.time.get_ticks() - self.bullet_cooldown >= 170:
            bullet = Bullet(
                self.images["bullet"],
                [12, 12],
                self.player.position.xy,
                self.rifle.angle,
                18,
            )
            self.player.ammo -= 1
            self.bullets.add(bullet)
            self.all_sprites.add(bullet)
            self.bullet_cooldown = pg.time.get_ticks()

    def spawn_ammo(self) -> None:
        if len(self.ammos) < 4:
            ammo_surface = pg.Surface((60, 60))
            ammo_surface.fill("red")
            ammo = Obtainable_Item(
                ammo_surface,
                (
                    random.randint(0, self.w),
                    random.randint(0, self.h),
                ),
            )
            self.all_sprites.add(ammo)
            self.ammos.add(ammo)

    def main_game(self) -> None:
        self.mousepos = pg.mouse.get_pos()

        if self.enemy.collision(self.player.rect):
            self.running = False

        if pg.time.get_ticks() - self.ammo_delay >= 6500:
            self.spawn_ammo()
            self.ammo_delay = pg.time.get_ticks()

        for ammo in self.ammos:
            if ammo.collision(self.player.rect):
                self.all_sprites.remove(ammo)
                self.ammos.remove(ammo)
                self.player.ammo += 15

        if pg.mouse.get_pressed() == (1, 0, 0) and self.player.ammo != 0:
            self.shoot()

        for bullet in self.bullets:
            bullet.update(self.background, self.dt)
            if bullet.hit(self.enemy.rect):
                self.enemy.health -= 1
                if self.enemy.health == 0:
                    self.enemy.kill()

                    self.enemy = Enemy(
                        [
                            random.randint(10, self.w - 10),
                            random.randint(10, self.h - 10),
                        ],
                        self.images["enemy"],
                        self.player.base_speed - 1.5,
                        self.matrix,
                        self.tile_x,
                        self.tile_y,
                        self.rows,
                        self.cols,
                    )
                    self.enemy.add(self.all_sprites)

                    self.player.kill_count += 1

                bullet.kill()
                self.bullets.remove(bullet)
                self.all_sprites.remove(bullet)

        self.player.update(self.dt, self.w, self.h)
        self.rifle.update(
            self.player.position,
        )
        self.enemy.update(self.dt, self.w, self.h, self.player, 500)

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

            self.screen.blit(self.background)

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
            # point = self.enemy.path[0][0]
            # pg.draw.circle(
            #     self.screen,
            #     "orange",
            #     (point.x * self.tile_x, point.y * self.tile_y),
            #     8,
            # )
            #
            # for col in range(self.cols + 1):
            #     x = col * self.tile_x
            #     pg.draw.line(self.screen, "purple", (x, 0), (x, self.h), 1)
            #
            # for row in range(self.rows + 1):
            #     y = row * self.tile_y
            #     pg.draw.line(self.screen, "purple", (0, y), (self.w, y), 1)
            #
            # pg.draw.rect(self.screen, "red", self.enemy.rect, 4)
            # pg.draw.rect(self.screen, "blue", self.enemy.rect, 4)

            pg.display.flip()

        pg.quit()
        sys.exit()


if __name__ == "__main__":
    matrix = np.ones((40, 40), dtype=int)
    main = Main(matrix, 32, 18, 40, 40)
    asyncio.run(main.main())
