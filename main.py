import pygame as pg
from pygame.locals import *
import sys
import math
from scripts.settings import *
from scripts.utilities import show_text, load_image
from scripts.entities import Player
from scripts.bullet import Bullet


class Main:
    def __init__(self) -> None:
        pg.init()

        pg.display.set_caption("unnamed game")
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
        self.bullet_cooldown = 10
        
    def shoot(self, dt) -> None:
        mousepos = pg.mouse.get_pos()

        self.angle = math.degrees(math.atan2(mousepos[1] - self.player.position.y, mousepos[0] - self.player.position.x)) 

        if self.bullet_cooldown == 0:
            bullet = Bullet([12, 8], self.player.position.xy, self.angle, 6, 'black')

            self.bullets.add(bullet)
            self.all_sprites.add(bullet)

            self.bullet_cooldown = 10

        else:
            self.bullet_cooldown -= 1


    def main_game(self, dt: float) -> None:
        self.background.fill((3, 200, 200))

        key = pg.key.get_pressed()
        if key[K_e]:
            self.shoot(dt)

        for bullet in self.bullets:
            bullet.update(dt, self.background)

        self.player.update(self.bg_size, dt, 5)

    def render(self) -> None:
        self.screen.blit(pg.transform.scale(self.background, SIZE), (0, 0))

        show_text(
                str(int(self.clock.get_fps())) + ' FPS',
                self.fps_font,
                "white",
                [5, 0],
                self.background,
            )

        for entity in self.all_sprites:
            self.background.blit(entity.image, entity.rect)

        pg.display.flip()

    def run(self) -> None:
        while True:

							 for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()

            self.dt = self.clock.tick(FPS) / 1000
            self.dt = min(0.03, max(0.01, self.dt))

            self.main_game(self.dt)

            self.render()


if __name__ == "__main__":
    main = Main()
    main.run()
