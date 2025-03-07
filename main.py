import pygame as pg
import sys
import random

from scripts.settings import *

class Main:
    def __init__(self):
        pg.init()

        pg.display.set_caption("unnamed game")
        self.screen = pg.display.set_mode(SIZE)

        self.clock = pg.time.Clock()

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def run(self):
        while True:
								screen.fill(BLACK)
            self.event_handler()
            pg.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    main = Main()
    main.run()

            


