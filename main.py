import pygame as pg
from pygame.locals import *
import sys
from scripts.settings import *
from scripts.utilities import show_text, load_image
from scripts.entities import Player
from scripts.bullet import Bullet


class Main:
    def __init__(self) -> None:
        pg.init()

        pg.display.set_caption("unnamed game")
        self.screen = pg.display.set_mode(SIZE)

        self.background = pg.Surface((600, 500))
        self.bg_size = self.background.get_size()

        self.fps_font = pg.font.SysFont("arial", 20)
        self.clock = pg.Clock()

        self.images = {"player": load_image(BASE_IMAGE_PATH + "player.png", "white")}

        self.player_pos = [self.bg_size[0] / 2, self.bg_size[1] / 2]
        self.player = Player(self.player_pos, self.images["player"])

        self.all_sprites = pg.sprite.Group(self.player)
        self.bullets = pg.sprite.Group()

        self.dt = 0.017
        self.bullet_cooldown = 0

    def event_handler(self) -> None:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

    def shoot(self, dt) -> None:
        if self.bullet_cooldown == 0:
            bullet = Bullet([12, 8], self.player.position.xy, 0, 45, 'black')
            bullet.update(dt, self.background)

            self.bullets.add(bullet)
            self.bullet_cooldown = 0.2
        else:
            self.bullet_cooldown -= dt / 100

    def main_game(self, dt: float) -> None:
        self.background.fill((3, 200, 200))

        key = pg.key.get_pressed()
        if key[K_e]:
            self.shoot(dt)

        self.player.update(self.bg_size, dt, 5)

    def run(self) -> None:
        while True:
            self.event_handler()
            self.dt = self.clock.tick(FPS) / 1000
            self.dt = min(0.03, max(0.001, self.dt)) * 100

            self.main_game(self.dt)

            show_text(
                str(int(self.clock.get_fps())) + ' FPS',
                self.fps_font,
                "white",
                [5, 0],
                self.screen,
            )

            for entity in self.all_sprites:
                self.background.blit(entity.image, entity.rect)

            self.screen.blit(pg.transform.scale(self.background, SIZE), (0, 0))
            pg.display.flip()

            print(len(self.all_sprites.sprites()))


if __name__ == "__main__":
    main = Main()
    main.run()
