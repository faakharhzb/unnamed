import numpy as np
import pygame as pg

import sys
import math
import random
import asyncio

from scripts.utilities import show_text, load_image
from scripts.entities import Player, Enemy
from scripts.objects import Bullet, Obtainable_Item, Gun
from scripts.camera import Camera


class Main:
    def __init__(self, matrix: np.ndarray | list) -> None:
        pg.init()
        pg.display.set_caption("Unnamed Game")
        self.screen = pg.display.set_mode((1280, 720))
        self.w, self.h = self.screen.get_size()

        self.images = {
            "player": load_image("player.png", "white", scale=3),
            "enemy": load_image("enemy.png", "white"),
            "rifle": load_image("guns/rifle.png", "white", scale=1.5),
            "background": load_image("background.png", "white"),
        }

        self.background = pg.transform.scale(
            self.images["background"], (self.w, self.h)
        )

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
            [random.randint(1, self.w), random.randint(1, self.h)],
            self.images["enemy"],
            self.player.base_speed - 1,
            matrix,
        )
        self.camera = Camera(self.player, pg.Vector2())
        self.all_sprites = pg.sprite.Group(self.player, self.rifle, self.enemy)
        self.bullets = pg.sprite.Group()
        self.ammos = pg.sprite.Group()

        self.dt = 0.017
        self.bullet_cooldown = pg.time.get_ticks()
        self.ammo_delay = pg.time.get_ticks()

        self.running = True

        self.matrix = matrix

    def shoot(self) -> None:
        self.mousepos = pg.mouse.get_pos()
        player_to_mouse_angle = math.degrees(
            math.atan2(
                self.mousepos[1] - self.player.position.y,
                self.mousepos[0] - self.player.position.x,
            )
        )
        if pg.time.get_ticks() - self.bullet_cooldown >= 170:
            bullet = Bullet(
                [12, 12],
                self.player.position.xy,
                player_to_mouse_angle,
                15,
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

        player_to_mouse_angle = math.degrees(
            math.atan2(
                self.mousepos[1] - self.player.position.y,
                self.mousepos[0] - self.player.position.x,
            )
        )

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

        show_text(
            f"Ammo: {self.player.ammo}",
            self.fps_font,
            "white",
            [5, 50],
            self.screen,
        )

        if pg.mouse.get_pressed() == (1, 0, 0) and self.player.ammo != 0:
            self.shoot()

        for bullet in self.bullets:
            bullet.update(self.background, self.dt)
            if bullet.hit(self.enemy.rect):
                self.enemy.kill()

                self.enemy = Enemy(
                    [
                        random.randint(10, self.w),
                        random.randint(10, self.h),
                    ],
                    self.images["enemy"],
                    self.player.base_speed - 1,
                    self.matrix,
                )
                self.enemy.add(self.all_sprites)

        self.player.update(self.dt, self.w, self.h)
        self.rifle.update(
            player_to_mouse_angle,
            (self.player.rect.centerx, self.player.rect.centery),
        )

        self.enemy.update(self.player, 240, self.dt, self.w, self.h)

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

            show_text(
                f"{int(self.clock.get_fps() // 1)} FPS",
                self.fps_font,
                "white",
                [5, 0],
                self.screen,
            )

            if hasattr(self.enemy, "path"):
                for node in self.enemy.path:
                    pg.draw.circle(
                        self.screen,
                        "black",
                        (
                            node.x * len(self.matrix[0]),
                            node.y * len(self.matrix[1]),
                        ),
                        10,
                    )

            pg.display.flip()

        pg.quit()
        sys.exit()


if __name__ == "__main__":
    matrix = np.ones((50, 50), dtype=int)
    main = Main(matrix)
    asyncio.run(main.main())
