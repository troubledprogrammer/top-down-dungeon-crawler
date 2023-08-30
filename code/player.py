import pygame as pg
from typing import Tuple

from code.settings import PLAYER_SIZE, PLAYER_SPEED


class Player(pg.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int] | pg.Vector2):
        super().__init__()
        self.image = pg.Surface(PLAYER_SIZE)
        self.image.fill("green")
        self.rect = self.image.get_rect(topleft=pos)

        self.velocity = pg.Vector2()
        self.lock_x = self.lock_y = False

    def _update_input(self, dt):
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.velocity.x = -PLAYER_SPEED * dt
        elif keys[pg.K_d]:
            self.velocity.x = PLAYER_SPEED * dt
        else:
            self.velocity.x = 0

        if keys[pg.K_w]:
            self.velocity.y = -PLAYER_SPEED * dt
        elif keys[pg.K_s]:
            self.velocity.y = PLAYER_SPEED * dt
        else:
            self.velocity.y = 0

    def update_movement_x(self):
        if not self.lock_x:
            self.rect.x += self.velocity.x

    def update_movement_y(self):
        if not self.lock_y:
            self.rect.y += self.velocity.y

    def update(self, dt):
        self._update_input(dt)

