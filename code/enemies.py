from __future__ import annotations

import pygame as pg
from typing import Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from code.window import Window

from code.settings import ASSETS_PATH_ENEMY, ENEMY_SIZE, ENEMY_SPEED, ENEMY_HITBOX_OFFSET_X, \
    ENEMY_HITBOX_OFFSET_Y, ENEMY_HITBOX_SIZE

class Enemy(pg.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int] | pg.Vector2):
        # super
        super().__init__()

        # visual
        self.image = pg.transform.scale(pg.image.load(ASSETS_PATH_ENEMY + "wogol_idle_anim_f0.png"), ENEMY_SIZE)

        # collisions
        self.rect = self.image.get_rect(topleft=pos)
        self.collide_rect = pg.Rect(*pos, *ENEMY_HITBOX_SIZE)
        self.reset_collide_rect_pos()

        # movement
        self.velocity = pg.Vector2(ENEMY_SPEED, ENEMY_SPEED)
        self.pos_on_map = pg.Vector2(pos)

        # damage
        self.damage_value = 5

    def _update_movement(self, dt: int):
        self.pos_on_map += self.velocity * dt
    
    def reset_collide_rect_pos(self):
        self.collide_rect.x = self.rect.x + ENEMY_HITBOX_OFFSET_X
        self.collide_rect.y = self.rect.y + ENEMY_HITBOX_OFFSET_Y

    def update(self, shift: pg.Vector2, window: Window) -> None:
        self._update_movement(window.deltatime)
        self.rect.topleft = self.pos_on_map + shift
        self.reset_collide_rect_pos()