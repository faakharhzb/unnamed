import pygame as pg
from pygame.locals import *

import sys

from scripts.settings import *
from scripts.utilities import *

class Main:
    def __init__(self):
        pg.init()

        pg.display.set_caption("unnamed game")
        self.screen = pg.display.set_mode(SIZE)

        self.clock = pg.time.Clock()

    def event_handler(self):
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.screen.fill(BLACK)
            self.event_handler()
            pg.display.update()
            self.dt = self.clock.tick(FPS) / 1000
            self.dt = min(self.dt, 3 / FPS)

if __name__ == "__main__":
    main = Main()
    main.run()

            


