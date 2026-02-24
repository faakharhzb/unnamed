import numpy as np
import pygame as pg

import random

from scripts.utilities import (
    get_random_position,
    load_image,
    load_images,
    load_audio,
)
from scripts.entities import Player, Enemy
from scripts.objects import Bullet, Obtainable_Item, Gun


class Game:
    def __init__(
        self,
        matrix: np.ndarray | list,
        tile_x: int,
        tile_y: int,
        rows: int,
        cols: int,
        screen: pg.Surface,
        game_start_delay: int,
        bg_rect: pg.Rect,
    ) -> None:
        self.matrix = matrix
        self.tile_x, self.tile_y = tile_x, tile_y
        self.rows, self.cols = rows, cols

        pg.init()

        self.screen = screen
        self.w, self.h = self.screen.get_size()

        self.bg_rect = bg_rect

        self.images = {
            "player_idle": load_images("player/idle", "white", scale=(5, 6)),
            "player_running": load_images(
                "player/running", "white", scale=(5, 6)
            ),
            "enemy": load_image("enemy.png", "white", scale=1.1),
            "rifle": load_image("guns/rifle.png", "white", scale=2.75),
            "bullet": load_image("bullet.png", "white", scale=2),
            "ammo": load_image("ammo.png", "white"),
        }
        self.audio = {
            "gunshot": load_audio("gunshot.ogg", 0.4),
            "empty_gun": load_audio("empty_gun.ogg", 0.7),
            "reload": load_audio("reload.ogg", 0.7),
        }

        self.images["ammo"] = pg.transform.scale(self.images["ammo"], (60, 54))

        self.fps_font = pg.Font(size=33)
        self.clock = pg.time.Clock()

        self.mousepos = pg.mouse.get_pos()

        self.player_images = {
            "idle": self.images["player_idle"],
            "running": self.images["player_running"],
        }
        self.player = Player(
            [self.w // 2, self.h // 2],
            self.player_images,
            6,
            matrix,
            tile_x,
            tile_y,
            rows,
            cols,
            250,
        )
        self.rifle = Gun(self.images["rifle"], self.player.rect.center)
        self.enemy = Enemy(
            get_random_position(
                self.player.position,
                self.images["enemy"].get_size(),
                325,
                self.bg_rect,
                matrix,
                tile_x,
                tile_y,
            ),
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

        self.bullet_cooldown = pg.time.get_ticks()
        self.ammo_delay = pg.time.get_ticks()
        self.new_enemy_delay = pg.time.get_ticks()
        self.game_start_delay = game_start_delay

        self.running = True
        self.spawn_new_enemy = False

        self.prev_fps = 0
        self.fps_text = pg.Surface((10, 10))

        self.prev_ammo = 0
        self.ammo_text = pg.Surface((10, 10))

        self.prev_kills = 0
        self.kills_text = pg.Surface((10, 10))

    def reset(self) -> None:
        self.all_sprites.empty()
        self.bullets.empty()
        self.ammos.empty()

        self.player.kill_count = 0
        self.player.ammo = 24
        self.player.position.update([self.w // 2, self.h // 2])
        self.player.set_flipped(False)
        self.all_sprites.add(self.player)

        self.spawn_enemy()

        self.all_sprites.add(self.rifle)

        self.prev_ammo = 0
        self.ammo_text = pg.Surface((10, 10))

        self.prev_kills = 0
        self.kills_text = pg.Surface((10, 10))

    def shoot(self) -> None:
        self.mousepos = pg.mouse.get_pos()

        if pg.time.get_ticks() - self.bullet_cooldown >= 170:
            bullet = Bullet(
                self.images["bullet"],
                self.player.position.xy,
                self.rifle.angle,
                25,
            )
            self.player.ammo -= 1
            self.bullets.add(bullet)
            self.all_sprites.add(bullet)
            self.bullet_cooldown = pg.time.get_ticks()

            sound = self.audio["gunshot"]
            sound.play()

    def spawn_ammo(self) -> None:
        if len(self.ammos) < 4:
            ammo = Obtainable_Item(
                self.images["ammo"],
                get_random_position(
                    pg.Vector2(),
                    self.images["ammo"].get_size(),
                    0,
                    self.bg_rect,
                    self.matrix,
                    self.tile_x,
                    self.tile_y,
                ),
            )
            self.all_sprites.add(ammo)
            self.ammos.add(ammo)

    def spawn_enemy(self) -> None:
        self.enemy = Enemy(
            get_random_position(
                self.player.position,
                self.images["enemy"].get_size(),
                325,
                self.bg_rect,
                self.matrix,
                self.tile_x,
                self.tile_y,
            ),
            self.images["enemy"],
            self.player.base_speed - 1,
            self.matrix,
            self.tile_x,
            self.tile_y,
            self.rows,
            self.cols,
        )
        self.enemy.add(self.all_sprites)
        self.spawn_new_enemy = False

    def manage_hit(self) -> None:
        self.enemy.health -= 1
        if self.enemy.health <= 0:
            self.player.kill_count += 1
            self.enemy.kill()

            self.new_enemy_delay = pg.time.get_ticks()
            self.spawn_new_enemy = True
            self.enemy = None

    def update(self, dt: float) -> bool:
        self.dt = dt

        if pg.time.get_ticks() - self.game_start_delay <= 250:
            return True

        self.mousepos = pg.mouse.get_pos()

        if self.enemy is not None:
            if self.enemy.collision(self.player.rect):
                return False

        if pg.time.get_ticks() - self.ammo_delay >= 6700:
            self.spawn_ammo()
            self.ammo_delay = pg.time.get_ticks()

        for ammo in self.ammos:
            if ammo.collision(self.player.rect):
                self.all_sprites.remove(ammo)
                self.ammos.remove(ammo)
                self.player.ammo += 12

                sound = self.audio["reload"]
                sound.play()

        if pg.mouse.get_pressed() == (1, 0, 0):
            if self.player.ammo >= 1:
                self.shoot()
            else:
                sound = self.audio["empty_gun"]
                sound.play()

        for bullet in self.bullets:
            if self.enemy is None:
                break

            bullet.update(self.bg_rect, self.dt)
            if bullet.hit(self.enemy.rect):
                self.manage_hit()
                bullet.kill()

        if self.spawn_new_enemy:
            if pg.time.get_ticks() - self.new_enemy_delay >= random.randint(
                250, 5000
            ):
                self.spawn_enemy()

        self.player.update(self.dt, self.bg_rect)
        self.rifle.update(
            self.player.position,
        )

        if self.enemy is not None:
            self.enemy.update(self.dt, self.bg_rect, self.player, 425)

        if self.player.moved:
            self.player.set_state("running")
        else:
            self.player.set_state("idle")

        if 90 <= self.rifle.angle <= 270:
            self.player.set_flipped(True)
        else:
            self.player.set_flipped(False)

        return True

    def render(self, display: pg.Surface) -> None:
        for entity in self.all_sprites:
            entity.draw(display)

        ammo = f"Ammo: {self.player.ammo}"
        if ammo != self.prev_ammo:
            self.ammo_text = self.fps_font.render(ammo, True, "white")

        self.prev_ammo = ammo

        display.blit(self.ammo_text, (5, 50))

        kills = f"Kills: {self.player.kill_count}"
        if kills != self.prev_kills:
            self.kills_text = self.fps_font.render(kills, True, "white")

        self.prev_kills = kills

        display.blit(
            self.kills_text,
            (5, 0),
        )
