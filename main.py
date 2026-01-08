import numpy as np
import pygame as pg

import sys
import random
import asyncio

from scripts.utilities import show_text, load_image
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
            "player": load_image("player.png", "white", scale=2.8),
            "enemy": load_image("enemy.png", "white", scale=1.1),
            "rifle": load_image("guns/rifle.png", "white", scale=1.5),
            "background": load_image("background.png", "white"),
        }

        self.background = pg.transform.scale(
            self.images["background"], (self.w, self.h)
        )
        self.bg_pos = pg.Vector2()

        self.fps_font = pg.font.SysFont("arial", 20)
        self.clock = pg.time.Clock()

        self.mousepos = pg.mouse.get_pos()

        self.player = Player(
            [self.w // 2, self.h // 2],
            self.images["player"],
            8,
        )
        self.rifle = Gun(self.images["rifle"], self.player.rect.center)
        self.enemy = Enemy(
            [
                random.randint(10, self.w - 10),
                random.randint(10, self.h - 10),
            ],
            self.images["enemy"],
            self.player.base_speed - 1,
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
        self.tile_x, self.tile_y = tile_x, tile_y
        self.rows, self.cols = rows, cols

    def shoot(self) -> None:
        self.mousepos = pg.mouse.get_pos()

        if pg.time.get_ticks() - self.bullet_cooldown >= 170:
            bullet = Bullet(
                [12, 12],
                self.player.position.xy,
                self.rifle.angle,
                18,
                "black",
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
                self.enemy.kill()

                self.enemy = Enemy(
                    [
                        random.randint(10, self.w - 10),
                        random.randint(10, self.h - 10),
                    ],
                    self.images["enemy"],
                    self.player.base_speed - 1,
                    self.matrix,
                    self.tile_x,
                    self.tile_y,
                    self.rows,
                    self.cols,
                )
                self.enemy.add(self.all_sprites)

        self.player.update(self.dt, self.w, self.h)
        self.rifle.update(
            self.player.position,
        )

        self.enemy.update(self.dt, self.w, self.h, self.player, 500)

    async def main(self) -> None:
        self.running = True
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            self.dt = (self.clock.tick() / 1000) * 60
            await asyncio.sleep(0)

            self.main_game()

            self.screen.blit(self.background, self.bg_pos)

            for entity in self.all_sprites:
                entity.draw(self.screen)

            show_text(
                f"{int(self.clock.get_fps() // 1)} FPS",
                self.fps_font,
                "white",
                [5, 0],
                self.screen,
            )
            show_text(
                f"Ammo: {self.player.ammo}",
                self.fps_font,
                "white",
                [5, 50],
                self.screen,
            )

            for point in self.enemy.path[0]:
                pg.draw.circle(
                    self.screen,
                    "black",
                    (
                        point.x * self.tile_x,
                        point.y * self.tile_y,
                    ),
                    5,
                )

            pg.draw.rect(self.screen, "red", self.player.rect, 5)
            pg.draw.rect(self.screen, "blue", self.enemy.rect, 5)
            pg.draw.circle(self.screen, "orange", self.enemy.target_pos, 7)

            for col in range(self.cols + 1):
                x = col * self.tile_x
                pg.draw.line(self.screen, "purple", (x, 0), (x, self.h), 1)

            for row in range(self.rows + 1):
                y = row * self.tile_y
                pg.draw.line(self.screen, "purple", (0, y), (self.w, y), 1)

            pg.display.flip()

        pg.quit()
        sys.exit()


if __name__ == "__main__":
    matrix = np.ones((40, 40), dtype=int)
    main = Main(matrix, 32, 18, 40, 40)
    asyncio.run(main.main())
