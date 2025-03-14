import pygame as pg
from pygame.locals import *
import sys
from scripts.settings import *
from scripts.utilities import show_text, load_image, load_images
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

        self.images = {
            "player": load_image(BASE_IMAGE_PATH + "player.png", "white"),
        }

        self.player_pos = [self.bg_size[0] / 2, self.bg_size[1] / 2]
        self.player = Player(
           self.player_pos , self.images["player"]
        )

        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.player)

        self.dt = 0.017

        self.base_speed = [0, 0]

    def event_handler(self) -> None:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

    def main_game(self, dt: float) -> None:
        self.background.fill((3, 200, 200))

        self.bg_size = list(self.background.get_size())

        self.player.update(self.bg_size,  dt, 3)
        key = pg.key.get_pressed()
        if key[K_e]:
            bullet = Bullet([50, 50], self.player_pos, "white", 0)
            bullet.update(dt, 100)
            pg.draw.rect(self.background, 'red', bullet.rect, 5)

        for sprite in self.all_sprites:
            self.background.blit(sprite.image, sprite.rect)
            pg.draw.rect(self.background, 'red', sprite.rect, 5)

        self.screen.blit(pg.transform.scale(self.background, SIZE), (0, 0))

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
            
            if self.player.velocity != self.base_speed:
                print('speed: ', self.player.velocity)
                self.base_speed = self.player.velocity

            pg.display.flip()


if __name__ == "__main__":
    main = Main()
    main.run()
