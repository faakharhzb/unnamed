import pygame as pg
from pygame.locals import QUIT
import sys
import math
import random

from scripts.settings import *
from scripts.utilities import show_text, load_image
from scripts.entities import Player
from scripts.objects import Bullet, Obtainable_Item, Gun


class Main:
    def __init__(self) -> None:
        pg.init()

        pg.display.set_caption("Unnamed Game")
        self.screen = pg.display.set_mode(SIZE, SCREEN_FLAGS)

        self.background = pg.Surface(SIZE)
        self.bg_size = self.background.get_size()

        self.fps_font = pg.font.SysFont("arial", 20)
        self.clock = pg.time.Clock()

        self.images = {
            "player": pg.transform.scale_by(
                load_image(BASE_IMAGE_PATH + "player.png", "white"), 1.3
            ),
            "rifle": load_image(BASE_IMAGE_PATH + "guns/rifle.png", (255, 255, 255)),
        }

        self.player = Player(
            [self.bg_size[0] / 2, self.bg_size[1] / 2], self.images["player"]
        )
        self.rifle = Gun(self.images["rifle"], self.player.rect.center)

        self.all_sprites = pg.sprite.Group(self.player, self.rifle)
        self.bullets = pg.sprite.Group()
        self.ammos = pg.sprite.Group()

        self.dt = 0.017
        self.bullet_cooldown = pg.time.get_ticks()
        self.ammo_delay = pg.time.get_ticks()

        self.mousepos = pg.mouse.get_pos()

        self.angle = math.degrees(
            math.atan2(
                self.mousepos[1] - self.player.position.y,
                self.mousepos[0] - self.player.position.x,
            )
        )

    def shoot(self) -> None:
        mousepos = pg.mouse.get_pos()

        if pg.time.get_ticks() - self.bullet_cooldown >= 170:
            bullet = Bullet(
                [12, 12], self.player.position.xy, self.angle, 700 * self.dt, "black"
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
                    random.randint(0, self.bg_size[0]),
                    random.randint(0, self.bg_size[1]),
                ),
            )
            self.all_sprites.add(ammo)
            self.ammos.add(ammo)

    def main_game(self) -> None:
        self.background.fill((3, 200, 200))
        self.mousepos = pg.mouse.get_pos()

        self.angle = math.degrees(
            math.atan2(
                self.mousepos[1] - self.player.position.y,
                self.mousepos[0] - self.player.position.x,
            )
        )

        if pg.time.get_ticks() - self.ammo_delay >= 5000:
            self.spawn_ammo()
            self.ammo_delay = pg.time.get_ticks()

        for ammo in self.ammos:
            if ammo.collision(self.player.rect):
                self.all_sprites.remove(ammo)
                self.ammos.remove(ammo)
                self.player.ammo += 20

        show_text(
            f"Ammo: {self.player.ammo}",
            self.fps_font,
            "white",
            [5, 50],
            self.background,
        )

        if pg.mouse.get_pressed() == (1, 0, 0) and self.player.ammo != 0:
            self.shoot()

        for bullet in self.bullets:
            bullet.update(self.background)

        self.player.update(self.bg_size, 400 * self.dt)

        self.rifle.update(self.angle, (self.player.rect.centerx, self.player.rect.centery))

    def run(self) -> None:
        while True:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()

            self.dt = self.clock.tick(FPS) / 1000

            self.main_game()

            for entity in self.all_sprites:
                entity.draw(self.background)

            show_text(
                f"{int(self.clock.get_fps())} FPS",
                self.fps_font,
                "white",
                [5, 0],
                self.background,
            )

            self.screen.blit(self.background, (0, 0))
            pg.display.flip()


if __name__ == "__main__":
    Main().run()
