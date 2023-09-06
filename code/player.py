import pygame as pg
from typing import Tuple

from code.settings import PLAYER_SIZE, PLAYER_SPEED, DEBUG


class Player(pg.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int] | pg.Vector2):
        super().__init__()
        self.image = pg.image.load("assets/characters/angel/angel_idle_anim_f0.png")
        self.image = pg.transform.scale(self.image, PLAYER_SIZE)
        self.rect = self.image.get_rect(center=pos)

        if DEBUG:
            pg.draw.rect(self.image, "red", pg.Rect(0, 0, *self.rect.size), 1)

        self.velocity = pg.Vector2()
        self.lock_x = self.lock_y = False

    def _update_input(self, dt):
        keys = pg.key.get_pressed()

        self.velocity.x = 0
        if keys[pg.K_a]:
            self.velocity.x += -PLAYER_SPEED * dt
        if keys[pg.K_d]:
            self.velocity.x += PLAYER_SPEED * dt

        self.velocity.y = 0
        if keys[pg.K_w]:
            self.velocity.y += -PLAYER_SPEED * dt
        if keys[pg.K_s]:
            self.velocity.y += PLAYER_SPEED * dt

    def update_movement_x(self):
        if not self.lock_x:
            self.rect.x += self.velocity.x

    def update_movement_y(self):
        if not self.lock_y:
            self.rect.y += self.velocity.y

    def update(self, dt):
        self._update_input(dt)

