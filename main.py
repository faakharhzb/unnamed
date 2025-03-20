import pygame as pg
from pygame.locals import *

import sys
import math
from time import time
from pathlib import Path
import os.path

from scripts.settings import *
from scripts.utilities import show_text, load_image
from scripts.entities import Player
from scripts.bullet import Bullet

class Main:
    def __init__(self) -> None:
        Path.cwd = os.path.dirname(__file__)

        pg.init()

        pg.display.set_caption("Unnamed Game")
        self.screen = pg.display.set_mode(SIZE, SCREEN_FLAGS)

        self.background = pg.Surface(SIZE)
        self.bg_size = self.background.get_size()

        self.fps_font = pg.font.SysFont("arial", 20)

        self.clock = pg.time.Clock()

        self.images = {"player": load_image(BASE_IMAGE_PATH + "player.png", "white")}

        self.player_pos = [self.bg_size[0] / 2, self.bg_size[1] / 2]
        self.player = Player(self.player_pos, self.images["player"])

        self.all_sprites = pg.sprite.Group(self.player)
        self.bullets = pg.sprite.Group()

        self.dt = 0.017
        self.bullet_cooldown = time() * 1000

    def shoot(self) -> None:
        mousepos = pg.mouse.get_pos()

        self.angle = math.degrees(math.atan2(mousepos[1] - self.player.position.y, mousepos[0] - self.player.position.x))

        current_time = time() * 1000

        if current_time - self.bullet_cooldown >= 300:
            bullet = Bullet([12, 8], self.player.position.xy, self.angle, 690 * self.dt, 'black')
            self.bullets.add(bullet)
            self.all_sprites.add(bullet)

            self.bullet_cooldown = time() * 1000


    def main_game(self) -> None:
        self.background.fill((3, 200, 200))

        key = pg.key.get_pressed()

        if key[K_e]:
            self.shoot()
        for bullet in self.bullets:
            bullet.update(self.background)

        self.player.update(self.bg_size, 400 * self.dt)

    def run(self) -> None:
        while True:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()

            self.dt = self.clock.tick(FPS) / 1000
            self.dt = min(0.03, max(0.01, self.dt))

            self.main_game()

            for entity in self.all_sprites:
                self.background.blit(entity.image, entity.rect)

            self.screen.blit(pg.transform.scale(self.background, SIZE), (0, 0))

            show_text(f"{int(self.clock.get_fps())} FPS", self.fps_font, "white", [5, 0], self.background)
            pg.display.flip()


if __name__ == "__main__":
    main = Main()
    main.run()
