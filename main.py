import pygame as pg
from pygame.locals import QUIT
import sys
import math
import random
from scripts.settings import *
from scripts.utilities import show_text, load_image
from scripts.entities import Player, Enemy
from scripts.objects import Bullet, Obtainable_Item, Gun
import asyncio


class Main:
    def __init__(self) -> None:
        pg.init()
        pg.display.set_caption('Unnamed Game')
        self.screen = pg.display.set_mode(SIZE, SCREEN_FLAGS)

        self.background = pg.Surface(SIZE)
        self.bg_size = self.background.get_size()

        self.fps_font = pg.font.SysFont('arial', 20)
        self.clock = pg.time.Clock()

        self.images = {
            'player': load_image('player.png', 'white', scale=3),
            'rifle': load_image('guns/rifle.png', (255, 255, 255), scale=1.5),
            'enemy': load_image('enemy.png', 'white'),
        }

        self.mousepos = pg.mouse.get_pos()

        self.player = Player(
            [self.bg_size[0] // 2, self.bg_size[1] // 2],
            self.images['player'],
            500,
        )
        self.rifle = Gun(self.images['rifle'], self.player.rect.center)
        self.enemy = Enemy(
            [random.randint(1, WIDTH), random.randint(1, HEIGHT)],
            self.images['enemy'],
            self.player.base_speed - 100,
            0,
        )
        self.all_sprites = pg.sprite.Group(self.player, self.rifle, self.enemy)
        self.bullets = pg.sprite.Group()
        self.ammos = pg.sprite.Group()

        self.dt = 0.017
        self.bullet_cooldown = pg.time.get_ticks()
        self.ammo_delay = pg.time.get_ticks()

        self.running = True

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
                840,
                'black',
            )
            self.player.ammo -= 1
            self.bullets.add(bullet)
            self.all_sprites.add(bullet)
            self.bullet_cooldown = pg.time.get_ticks()

    def spawn_ammo(self) -> None:
        if len(self.ammos) < 4:
            ammo_surface = pg.Surface((60, 60))
            ammo_surface.fill('red')
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

        player_to_mouse_angle = math.degrees(
            math.atan2(
                self.mousepos[1] - self.player.position.y,
                self.mousepos[0] - self.player.position.x,
            )
        )
        enemy_to_player_angle = math.degrees(
            math.atan2(
                self.player.position.y - self.enemy.position.y,
                self.player.position.x - self.enemy.position.x,
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
            f'Ammo: {self.player.ammo}',
            self.fps_font,
            'white',
            [5, 50],
            self.background,
        )

        if pg.mouse.get_pressed() == (1, 0, 0) and self.player.ammo != 0:
            self.shoot()

        for bullet in self.bullets:
            bullet.update(self.background, self.dt)
            if bullet.hit(self.enemy.rect):
                self.enemy.kill()

                self.enemy = Enemy(
                    [
                        random.randint(1, WIDTH),
                        random.randint(1, HEIGHT),
                    ],
                    self.images['enemy'],
                    self.player.base_speed - 44,
                    0,
                )
                self.enemy.add(self.all_sprites)

        self.player.update(self.dt)
        self.rifle.update(
            player_to_mouse_angle,
            (self.player.rect.centerx, self.player.rect.centery),
        )

        self.enemy.update(self.player, 240, enemy_to_player_angle, self.dt)

    async def main(self) -> None:
        self.running = True
        while self.running:
            for event in pg.event.get():
                if event.type == QUIT:
                    self.running = False

            self.dt = self.clock.tick(FPS) / 1000
            await asyncio.sleep(0)

            self.main_game()

            for entity in self.all_sprites:
                entity.draw(self.background)

            show_text(
                f'{int(self.clock.get_fps() // 1)} FPS',
                self.fps_font,
                'white',
                [5, 0],
                self.background,
            )

            self.screen.blit(self.background, (0, 0))
            pg.display.flip()

        pg.quit()
        sys.exit()


if __name__ == '__main__':
    main = Main()
    asyncio.run(main.main())
